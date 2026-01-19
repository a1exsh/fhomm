from collections import namedtuple

import pygame

from fhomm.render import Pos, Size, Rect
import fhomm.handler
import fhomm.render

DEBUG_RENDER = False
DEBUG_EVENTS = False


class Element(object):

    State = namedtuple('State', [], module='fhomm.ui.Element')

    def __init__(self, size, state=State()):
        self.size = size
        self.initial_state = state

        self.hovered = False    # TODO: should be part of the state
        self._dirty = False

    @property
    def rect(self):
        return Rect.of(self.size)

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

    @staticmethod
    def is_mouse_event(event):
        return event.type in [
            pygame.MOUSEMOTION,
            pygame.MOUSEBUTTONDOWN,
            pygame.MOUSEBUTTONUP,
            pygame.MOUSEWHEEL,
        ]

    @staticmethod
    def translate_event(event, origin_pos):
        if Element.is_mouse_event(event):
            return Element.translate_mouse_event(event, origin_pos)

        else:
            return event

    @staticmethod
    def translate_mouse_event(event, origin_pos):
        return pygame.event.Event(
            event.type,
            dict(
                event.__dict__,
                pos=(
                    event.pos[0] - origin_pos.x,
                    event.pos[1] - origin_pos.y,
                ),
            ),
        )

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
            return self.on_mouse_move(pos, relpos, event.buttons)

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

    def on_mouse_move(self, pos, rel, buttons):
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


def asseq(cmd):
    # print(f"asseq: {cmd}")
    if cmd is None:
        return []

    elif isinstance(cmd, fhomm.handler.Command):
        return [cmd]

    else:
        return [c for c in cmd if c] # filter out Nones


class Window(Element):
    #
    # We externalize the state key so that an element cannot accidentally
    # affect state of an unrelated element.
    #
    class Slot(
        namedtuple('ChildSlot', ['element', 'relpos', 'key'], module='fhomm.ui')
    ):
        __slots__ = ()

        @property
        def rect(self):
            return Rect.of(self.element.size, self.relpos)

    def __init__(self, bg_image, child_slots=[], border_width=0):
        super().__init__(bg_image.size)

        self.bg_image = bg_image
        self.child_slots = child_slots
        self.border_width = border_width

        self.content_rect = Rect.of(
            Size(
                self.size.w - 2*border_width,
                self.size.h - 2*border_width,
            ),
            Pos(border_width, border_width),
        )

        self.initial_state_map = {
            child.key: child.element.initial_state
            for child in self.child_slots
        }
        self.initial_state_map['_self'] = self.initial_state

    def render(self, ctx, state, force=False):
        update = super().render(ctx, state['_self'], force)
        if update:
            force = True

        with ctx.restrict(self.content_rect) as content_ctx:
            for child in self.child_slots:
                with ctx.restrict(child.rect) as child_ctx:
                    if child.element.render(child_ctx, state[child.key], force):
                        update = True

        return update

    def on_render(self, ctx, _):
        self.bg_image.render(ctx)
        
    def handle(self, event):
        # TODO: input focus?
        cmd = self.on_event(event)
        if cmd:
            return [self.cmd_with_key('_self', c) for c in asseq(cmd)]

        commands = []

        for child in self.child_slots:
            cmd = self.handle_by_child(child, event)
            commands.extend(self.cmd_with_key(child.key, c) for c in asseq(cmd))

        return commands

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
                    Element.translate_mouse_event(event, child.relpos)
                )

        else:
            return child.element.handle(event)

    @staticmethod
    def cmd_with_key(key, cmd):
        print(f"cmd_with_key: {key} {cmd}")
        if cmd.code == fhomm.handler.UPDATE:
            return fhomm.handler.Command(
                fhomm.handler.UPDATE,
                dict(cmd.kwargs, key=key),
            )

        else:
            return cmd
