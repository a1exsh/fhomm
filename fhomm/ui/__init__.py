from collections import namedtuple

import pygame

from fhomm.render import Pos, Size, Rect
import fhomm.handler
import fhomm.render

DEBUG_RENDER = False
DEBUG_EVENTS = False


class Element(object):

    # NoState = namedtuple('NoState', [])

    def __init__(self, size): #, make_state=NoState):
        self.size = size
        # self.make_state = make_state

        self.parent = None
        self.hovered = False
        self._dirty = False

    @property
    def rect(self):
        return Rect.of(self.size)

    def on_attach(self, parent):
        pass

    def on_detach(self):
        pass

    def dirty(self):
        self._dirty = True

    def render(self, ctx, state, force=False):
        if self._dirty:
            self._dirty = False
            force = True

        if force:
            self.on_render(ctx, state)

            if DEBUG_RENDER and self.hovered:
                ctx.draw_rect(228, self.rect, 1)

            return True         # rendered, tell to update the screen

        return False

    def on_render(self, ctx, state):
        pass

    def handle(self, event):
        if DEBUG_EVENTS and event.type != fhomm.handler.EVENT_TICK:
            print(f"{self}.handle: {event}")

        return self.on_event(event)

    # def post_command(self, cmd):
    #     pygame.event.post(pygame.event.Event(fhomm.handle.EVENT_COMMAND, cmd=cmd))

    @classmethod
    def is_mouse_event(cls, event):
        return event.type in [
            pygame.MOUSEMOTION,
            pygame.MOUSEBUTTONDOWN,
            pygame.MOUSEBUTTONUP,
            pygame.MOUSEWHEEL,
        ]

    # on_event is low level, better define one of the more specific on_XXX
    def on_event(self, event):
        #print(f"{self}.on_event: {event}")

        if event.type == fhomm.handler.EVENT_TICK:
            return self.on_tick(event.dt)

        elif Element.is_mouse_event(event):
            return self.handle_mouse_event(event)

        elif event.type == pygame.KEYDOWN:
            return self.on_key_down(event.key)

        elif event.type == pygame.KEYUP:
            return self.on_key_up(event.key)

        elif event.type == pygame.QUIT:
            return self.on_quit()

        elif event.type == fhomm.handler.EVENT_WINDOW_CLOSED:
            return self.on_window_closed()

    def handle_mouse_event(self, event):
        pos = Pos(event.pos[0], event.pos[1])

        if event.type == pygame.MOUSEMOTION:
            old, self.hovered = self.hovered, self.rect.contains(pos)
            if old != self.hovered:
                if DEBUG_RENDER:
                    self.dirty()

                if self.hovered:
                    return self.on_mouse_enter()
                else:
                    return self.on_mouse_leave()

            relpos = Pos(event.rel[0], event.rel[1])
            return self.on_mouse_move(pos, relpos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            #print(f"mousedown: {event}")
            if event.button == 4 or event.button == 5:
                pass

            else:
                return self.on_mouse_down(pos, event.button)

        elif event.type == pygame.MOUSEBUTTONUP:
            #print(f"mouseup: {event}")
            if event.button == 4:
                return self.on_mouse_wheel(pos, 0, -1)

            elif event.button == 5:
                return self.on_mouse_wheel(pos, 0, 1)

            else:
                return self.on_mouse_up(pos, event.button)

        elif event.type == pygame.MOUSEWHEEL:
            # print(f"mousewheel: {event}")
            return self.on_mouse_wheel(mouse_pos, event.x, event.y)

    def on_tick(self, dt):
        pass

    def on_mouse_enter(self):
        pass

    def on_mouse_leave(self):
        pass

    def on_mouse_move(self, pos, relpos):
        pass

    def on_mouse_down(self, pos, button):
        pass

    def on_mouse_up(self, pos, button):
        pass

    def on_mouse_wheel(self, pos, dx, dy):
        pass

    def on_key_down(self, key):
        pass

    def on_key_up(self, key):
        pass

    def on_quit(self):
        #return fhomm.handler.CMD_IGNORE
        pass

    def on_window_closed(self):
        pass


class Container(Element):

    class ChildSlot(object):
        def __init__(self, element, relpos, key):
            self.element = element
            self.relpos = relpos
            self.key = key

        @property
        def rect(self):
            return Rect.of(self.element.size, self.relpos)

    def __init__(self, size): #, make_state=Element.NoState):
        super().__init__(size) #, make_state)
        self.child_slots = []

    def attach(self, element, relpos, key=None): #, state=None):
        if element.parent is not None:
            raise Exception(f"The UI element {element} is already attached to {parent}!")

        element.parent = self
        element.on_attach(self)

        # if state is None:
        #     state = element.make_state()

        self.child_slots.append(Container.ChildSlot(element, relpos, key))

    def detach(self, element):
        if self is not element.parent:
            raise Exception(f"The UI element {element} is not attached to {self}!")

        self.child_slots = [
            child
            for child in self.child_slots
            if element is not child.element
        ]
        element.on_detach()
        element.parent = None

    def render(self, ctx, state, force=False):
        update = super().render(ctx, state, force)
        if update:
            force = True

        for child in self.child_slots:
            if self.render_child(child, ctx, state, force):
                update = True

        return update

    def render_child(self, child, ctx, state, force=True):
        with ctx.restrict(child.rect) as child_ctx:
            if child.key:
                child_state = state[child.key]
            else:
                child_state = state
            return child.element.render(child_ctx, child_state, force)

    def handle(self, event):
        # TODO: input focus?
        cmd = self.on_event(event)
        if cmd is not None:
            return cmd

        commands = []

        for child in self.child_slots:
            cmd = self.handle_by_child(child, event)
            if cmd:
                if isinstance(cmd, fhomm.handler.Command):
                    commands.append(self.cmd_from_child(child, cmd))
                else:
                    commands.extend(
                        self.cmd_from_child(child, c)
                        for c in cmd
                    )

        return commands

    def cmd_from_child(self, child, cmd):
        if cmd.code == fhomm.handler.UPDATE and child.key:
            cmd = fhomm.handler.Command(
                fhomm.handler.UPDATE,
                {
                    'fn': cmd.kwargs['fn'],
                    'ks': [child.key, *cmd.kwargs.get('ks', [])],
                }
            )

        return cmd

    def handle_by_child(self, child, event):
        if Element.is_mouse_event(event):
            cur_pos = Pos(event.pos[0], event.pos[1])
            if event.type == pygame.MOUSEMOTION:
                old_pos = Pos(
                    event.pos[0] - event.rel[0],
                    event.pos[1] - event.rel[1],
                )
            else:
                old_pos = None

            if child.rect.contains(cur_pos) or \
               (old_pos is not None and child.rect.contains(old_pos)):
                return child.element.handle(
                    Container.translate_mouse_event(event, child.relpos),
                )

        else:
            return child.element.handle(event)

    @classmethod
    def translate_mouse_event(cls, event, child_pos):
        return pygame.event.Event(
            event.type,
            {
                **event.__dict__,
                'pos': (
                    event.pos[0] - child_pos.x,
                    event.pos[1] - child_pos.y,
                ),
            },
        )


class Window(Container):
    def __init__(self, state_key, bg_image, border_width):
        super().__init__(bg_image.size)
        self.bg_image = bg_image
        self.border_width = border_width

        self.container = Container(
            Size(
                self.size.w - 2*border_width,
                self.size.h - 2*border_width,
            )
        )
        super().attach(
            self.container,
            Pos(border_width, border_width),
            state_key,
        )

    def attach(self, element, relpos, key=None):
        self.container.attach(
            element,
            relpos.moved_by(Pos(-self.border_width, -self.border_width)),
            key,
        )

    def on_render(self, ctx, _):
        self.bg_image.render(ctx)
