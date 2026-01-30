from collections import namedtuple

import pygame

from fhomm.render import Pos, Size, Rect
import fhomm.command
import fhomm.render

DEBUG_RENDER = False
DEBUG_EVENTS = False

HOLD_TICKS_REPEAT_DELAY = 250
HOLD_TICKS_REPEAT_EVERY = 50


class Element(object):

    State = namedtuple('State', [], module='fhomm.ui.Element')

    def __init__(self, size, state=State(), mouse_grab=False):
        # print(f"{self.__class__}: {size} {state}")
        self.size = size
        self.initial_state = state
        self.mouse_grab = mouse_grab

        self.is_hovered = False    # TODO: should be part of the state
        self.hold_event = None

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

            if DEBUG_RENDER and self.is_hovered:
                ctx.draw_rect(228, self.rect, 1)

            return True         # rendered, tell to update the screen

        return False

    def on_render(self, ctx, state):
        pass

    def handle(self, event):
        if DEBUG_EVENTS and event.type != fhomm.command.EVENT_TICK:
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
        # if event.type != fhomm.command.EVENT_TICK:
        #     print(f"{self}.on_event: {event}")

        if event.type == fhomm.command.EVENT_TICK:
            if self.hold_event is not None:
                cmds = fhomm.command.asseq(self.on_hold(event.dt))
            else:
                cmds = []
            return cmds + fhomm.command.asseq(self.on_tick(event.dt))

        elif Element.is_mouse_event(event):
            return self.handle_mouse_event(event)

        elif event.type == pygame.KEYDOWN:
            if self.hold_event is None:
                self.start_hold(event)

            return self.on_key_down(event.key)

        elif event.type == pygame.KEYUP:
            if self.is_key_held(event.key):
                self.stop_hold()

            return self.on_key_up(event.key)

        elif event.type == pygame.QUIT:
            return self.on_quit()

        elif event.type == fhomm.command.EVENT_WINDOW_CLOSED:
            return self.on_window_closed(event.return_key, event.return_value)

    def handle_mouse_event(self, event):
        pos = Pos(event.pos[0], event.pos[1])

        if event.type == pygame.MOUSEMOTION:
            old, self.is_hovered = self.is_hovered, self.rect.contains(pos)
            if old != self.is_hovered:
                if DEBUG_RENDER:
                    self.dirty()

                if self.is_hovered:
                    return self.on_mouse_enter()

                else:
                    if self.is_mouse_held() and not self.mouse_grab:
                        self.stop_hold()

                    return self.on_mouse_leave()

            relpos = Pos(event.rel[0], event.rel[1])
            return self.on_mouse_move(pos, relpos, event.buttons)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            #print(f"mousedown: {event}")
            if event.button == 4 or event.button == 5:
                pass

            else:
                if self.hold_event is None:
                    self.start_hold(event)

                return self.on_mouse_down(pos, event.button)

        elif event.type == pygame.MOUSEBUTTONUP:
            #print(f"mouseup: {event}")
            if event.button == 4:
                return self.on_mouse_wheel(pos, 0, -1)

            elif event.button == 5:
                return self.on_mouse_wheel(pos, 0, 1)

            elif self.is_mouse_held(event.button):
                self.stop_hold()

                return self.on_mouse_up(pos, event.button)

        elif event.type == pygame.MOUSEWHEEL:
            # print(f"mousewheel: {event}")
            return self.on_mouse_wheel(mouse_pos, event.x, event.y)

    def start_hold(self, event):
        # print(f"start_hold: {event}")
        self.hold_event = event
        self.hold_ticks = -HOLD_TICKS_REPEAT_DELAY

    def stop_hold(self):
        # print(f"stop_hold: {self.hold_event}")
        self.hold_event = None
        self.hold_ticks = 0

    def is_key_held(self, key=None):
        return self.hold_event is not None and \
            self.hold_event.type == pygame.KEYDOWN and \
            (key is None or self.hold_event.key == key)

    def is_mouse_held(self, button=None):
        return self.hold_event is not None and \
            self.hold_event.type == pygame.MOUSEBUTTONDOWN and \
            (button is None or self.hold_event.button == button)

    def on_hold(self, dt):
        commands = []

        self.hold_ticks += dt
        while self.hold_ticks >= HOLD_TICKS_REPEAT_EVERY:
            self.hold_ticks -= HOLD_TICKS_REPEAT_EVERY

            if self.hold_event.type == pygame.KEYDOWN:
                cmds = self.on_key_hold(self.hold_event.key)

            elif self.hold_event.type == pygame.MOUSEBUTTONDOWN:
                cmds = self.on_mouse_hold(self.hold_event.button)

            else:
                cmds = None

            commands.extend(fhomm.command.asseq(cmds))

        return commands

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

    def on_mouse_hold(self, button):
        pass

    def on_mouse_up(self, pos, button):
        pass

    def on_mouse_wheel(self, pos, dx, dy):
        pass

    def on_key_down(self, key):
        pass

    def on_key_hold(self, key):
        pass

    def on_key_up(self, key):
        pass

    def on_quit(self):
        #return fhomm.command.CMD_IGNORE
        pass

    def on_window_closed(self, key, value):
        pass


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

    def __init__(
            self,
            bg_image,
            child_slots=[],
            border_width=0,
            state=Element.State()
    ):
        # a window must grab the mouse, otherwise it can lead to elements
        # getting input after mouse leaves and returns to the window area:
        super().__init__(bg_image.size, state, mouse_grab=True)

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
            '_self': self.initial_state,
        }
        for child in self.child_slots:
            if child.key not in self.initial_state_map:
                # first write wins!
                self.initial_state_map[child.key] = child.element.initial_state

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
        # if mouse is held, only the active element must be able to handle
        is_mouse_held = self.is_mouse_held() or \
            any(child.element.is_mouse_held() for child in self.child_slots)

        commands = []

        for child in self.child_slots:
            cmd = self.handle_by_child(is_mouse_held, child, event)
            commands.extend(
                self.cmd_with_key(child.key, c)
                for c in fhomm.command.asseq(cmd)
            )

        # TODO: are there situations where the window would want to handle
        # events before any child?
        #
        # TODO: input focus?
        cmd = self.on_event(event)
        commands.extend(
            self.cmd_with_key('_self', c)
            for c in fhomm.command.asseq(cmd)
        )

        return commands

    def handle_by_child(self, is_mouse_held, child, event):
        if Element.is_mouse_event(event):
            return self.handle_mouse_by_child(is_mouse_held, child, event)

        else:
            return child.element.handle(event)

    def handle_mouse_by_child(self, is_mouse_held, child, event):
        if is_mouse_held:
            should_handle = child.element.is_mouse_held()

        else:
            cur_pos = Pos(event.pos[0], event.pos[1])

            if event.type == pygame.MOUSEMOTION:
                old_pos = Pos(
                    event.pos[0] - event.rel[0],
                    event.pos[1] - event.rel[1],
                )

            else:
                old_pos = None

            should_handle = child.rect.contains(cur_pos) or \
                (old_pos is not None and child.rect.contains(old_pos))

        if should_handle:
            return child.element.handle(
                Element.translate_mouse_event(event, child.relpos)
            )

    @staticmethod
    def cmd_with_key(key, cmd):
        # print(f"cmd_with_key: {key} {cmd}")
        if cmd.code == fhomm.command.UPDATE and 'key' not in cmd.kwargs:
            return fhomm.command.Command(
                fhomm.command.UPDATE,
                dict(cmd.kwargs, key=key),
            )

        else:
            return cmd

    def make_return_value(self, state):
        pass
