from collections import namedtuple

import pygame

from fhomm.render import Pos, Size, Rect
import fhomm.command
import fhomm.event
import fhomm.render

DEBUG_RENDER = False
DEBUG_EVENTS = False

HOLD_TICKS_REPEAT_DELAY = 250
HOLD_TICKS_REPEAT_EVERY = 50


def state_tuple(fields=[], defaults=[], submodule='', **kwargs):

    class State(
        namedtuple(
            'State',
            fields + [
                'is_active',
                'is_hovered',
                'is_highlighted',
                'hold_event',
                'hold_ticks',
            ],
            defaults=(defaults + [True, False, False, None, 0]),
            module=('fhomm.ui.' + submodule),
            **kwargs
        )
    ):
        __slots__ = ()

        @staticmethod
        def active(s):
            return s._replace(is_active=True)

        @staticmethod
        def inactive(s):
            return s._replace(is_active=False)

        @staticmethod
        def hovered(s):
            return s._replace(is_hovered=True)

        @staticmethod
        def unhovered(s):
            return s._replace(is_hovered=False)

        @staticmethod
        def highlighted(s):
            return s._replace(is_highlighted=True)

        @staticmethod
        def dehighlighted(s):
            return s._replace(is_highlighted=False)

        @staticmethod
        def start_hold(event):
            return lambda s: s._replace(
                hold_event=event,
                hold_ticks=-HOLD_TICKS_REPEAT_DELAY,
            )

        @staticmethod
        def stop_hold(s):
            return s._replace(hold_event=None, hold_ticks=0)

        @staticmethod
        def set_hold_ticks(ticks):
            return lambda s: s._replace(hold_ticks=ticks)

    return State


class Element(object):

    State = state_tuple(submodule='Element')

    def __init__(self, size, state=State(), grabs_mouse=False):
        # print(f"{self.__class__}: {size} {state}")
        self.size = size
        self.initial_state = state
        self.grabs_mouse = grabs_mouse

        self._dirty = False

    @property
    def rect(self):
        return Rect.of(self.size)

    def dirty(self):
        self._dirty = True

    def render(self, ctx, state, ext_state=None, force=False):
        if self._dirty:
            self._dirty = False
            force = True

        if force:
            if ext_state is not None:
                self.on_render(ctx, state, ext_state)

            else:
                self.on_render(ctx, state)

            if DEBUG_RENDER:
                self.on_render_debug(ctx, state)

            return True         # rendered, tell to update the screen

        return False

    def on_render_debug(self, ctx, state):
        outline_color = None

        if state.is_highlighted:
            outline_color = 224

        if state.is_hovered:
            outline_color = 228

        if outline_color is not None:
            ctx.draw_rect(outline_color, self.rect, 1)

    def on_render(self, ctx, state, ext_state=None):
        pass

    def handle(self, state, event):
        if DEBUG_EVENTS and event.type != fhomm.event.EVENT_TICK:
            print(f"{self}.handle: {event}") # {state}

        if state.is_active:
            return self.on_event(state, event)

    @staticmethod
    def is_keyboard_event(event):
        return event.type in [pygame.KEYDOWN, pygame.KEYUP]

    @staticmethod
    def is_mouse_event(event):
        return event.type in [
            pygame.MOUSEMOTION,
            pygame.MOUSEBUTTONDOWN,
            pygame.MOUSEBUTTONUP,
            # pygame.MOUSEWHEEL,
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
    def on_event(self, state, event):
        # if event.type != fhomm.event.EVENT_TICK:
        #     print(f"{self}.on_event: {event}")

        if event.type == fhomm.event.EVENT_TICK:
            if state.hold_event is not None:
                cmds = fhomm.command.aslist(self.on_hold(state, event.dt))
            else:
                cmds = []

            return cmds + fhomm.command.aslist(self.on_tick(event.dt))

        elif Element.is_keyboard_event(event):
            return self.handle_keyboard_event(state, event)

        elif Element.is_mouse_event(event):
            return self.handle_mouse_event(state, event)

        elif event.type == pygame.QUIT:
            return self.on_quit()

        elif event.type == fhomm.event.EVENT_WINDOW_CLOSED:
            return self.on_window_closed(event.return_key, event.return_value)

    def handle_keyboard_event(self, state, event):
        if event.type == pygame.KEYDOWN:
            cmds = fhomm.command.aslist(self.on_key_down(event.key))

            if event.key == pygame.K_LCTRL:
                cmds.append(fhomm.command.cmd_update(Element.State.highlighted))

            if state.hold_event is None: # start_hold could also check that
                cmds.append(fhomm.command.cmd_update(Element.State.start_hold(event)))

            return cmds

        elif event.type == pygame.KEYUP:
            cmds = fhomm.command.aslist(self.on_key_up(event.key))

            if event.key == pygame.K_LCTRL:
                cmds.append(fhomm.command.cmd_update(Element.State.dehighlighted))

            if Element.is_key_held(state, event.key):
                cmds.append(fhomm.command.cmd_update(Element.State.stop_hold))

            return cmds

    def handle_mouse_event(self, state, event):
        pos = Pos(event.pos[0], event.pos[1])

        if event.type == pygame.MOUSEMOTION:
            is_hovered_now = self.rect.contains(pos)

            if state.is_hovered != is_hovered_now:
                if DEBUG_RENDER:
                    self.dirty() # TODO: remove

                if is_hovered_now:
                    cmds = fhomm.command.aslist(self.on_mouse_enter())
                    cmds.append(fhomm.command.cmd_update(Element.State.hovered))

                    return cmds

                else:
                    # FIXME: wrapping everything in `aslist()` is getting old..
                    cmds = fhomm.command.aslist(self.on_mouse_leave())
                    cmds.append(fhomm.command.cmd_update(Element.State.unhovered))

                    if Element.is_mouse_held(state) and not self.grabs_mouse:
                        cmds.append(fhomm.command.cmd_update(Element.State.stop_hold))

                    return cmds

            else:               # motion within the element rect
                relpos = Pos(event.rel[0], event.rel[1])
                return self.on_mouse_move(pos, relpos, event.buttons)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4 or event.button == 5: # mouse wheel
                pass

            else:
                cmds = fhomm.command.aslist(self.on_mouse_down(pos, event.button))

                if state.hold_event is None:
                    cmds.append(fhomm.command.cmd_update(Element.State.start_hold(event)))

                return cmds

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 4:
                return self.on_mouse_wheel(pos, 0, -1)

            elif event.button == 5:
                return self.on_mouse_wheel(pos, 0, 1)

            else:
                cmds = fhomm.command.aslist(self.on_mouse_up(pos, event.button))

                if Element.is_mouse_held(state, event.button):
                    cmds.append(fhomm.command.cmd_update(Element.State.stop_hold))

                return cmds

        # elif event.type == pygame.MOUSEWHEEL:
        #     return self.on_mouse_wheel(pos, event.x, event.y)

    @staticmethod
    def is_key_held(state, key=None):
        return state.hold_event is not None and \
            state.hold_event.type == pygame.KEYDOWN and \
            (key is None or state.hold_event.key == key)

    @staticmethod
    def is_mouse_held(state, button=None):
        return state.hold_event is not None and \
            state.hold_event.type == pygame.MOUSEBUTTONDOWN and \
            (button is None or state.hold_event.button == button)

    def on_hold(self, state, dt):
        commands = []

        ticks = state.hold_ticks + dt
        while ticks >= HOLD_TICKS_REPEAT_EVERY:
            ticks -= HOLD_TICKS_REPEAT_EVERY

            if state.hold_event.type == pygame.KEYDOWN:
                cmds = self.on_key_hold(state.hold_event.key)

            elif state.hold_event.type == pygame.MOUSEBUTTONDOWN:
                cmds = self.on_mouse_hold(state.hold_event.button)

            else:
                cmds = None

            commands.extend(fhomm.command.aslist(cmds))

        commands.append(fhomm.command.cmd_update(Element.State.set_hold_ticks(ticks)))

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
        if value is not None:
            return self.on_return(key, value)

    def on_return(self, key, value):
        pass


class Window(Element):
    class Slot(
        namedtuple(
            'ChildSlot',
            ['element', 'relpos', 'int_key', 'ext_key'],
            defaults=[None],
            module='fhomm.ui',
        )
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
            state=Element.State(),
    ):
        # a window must grab the mouse, otherwise it can lead to elements
        # getting input after mouse leaves and returns to the window area:
        super().__init__(bg_image.size, state, grabs_mouse=True)

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
            if child.int_key not in self.initial_state_map:
                # first write wins!
                self.initial_state_map[child.int_key] = child.element.initial_state

    def render(self, ctx, state_map, force=False):
        update = super().render(ctx, state_map['_self'], ext_state=None, force=force)
        if update:
            force = True

        with ctx.restrict(self.content_rect) as content_ctx:
            for child in self.child_slots:
                with ctx.restrict(child.rect) as child_ctx:
                    ext_state = state_map[child.ext_key] if child.ext_key else None
                    if child.element.render(
                            child_ctx,
                            state_map[child.int_key],
                            ext_state,
                            force,
                    ):
                        update = True

        return update

    def on_render(self, ctx, _):
        self.bg_image.render(ctx)

    def handle(self, state_map, event):
        # why does this stand out so much?
        if event.type == fhomm.event.EVENT_STATE_UPDATED:
            return self.on_update(event.key, event.old, event.new)

        # if mouse is held, only the active element must be able to handle
        self_mouse_held = Element.is_mouse_held(state_map['_self'])
        is_mouse_held = self_mouse_held or \
            any(
                Element.is_mouse_held(state_map[child.int_key])
                for child in self.child_slots
            )
        # print(f"self_mouse_held: {self_mouse_held} / is_mouse_held: {is_mouse_held}")

        commands = []

        for child in self.child_slots:
            child_state = state_map[child.int_key]

            cmd = self.handle_by_child(is_mouse_held, child, child_state, event)
            commands.extend(
                self.cmd_with_key(child.int_key, child.ext_key, c)
                for c in fhomm.command.aslist(cmd)
            )

        # skip processing if someone else's grabbed the mouse input
        if is_mouse_held and not self_mouse_held:
            return commands

        # TODO: are there situations where the window would want to handle
        # events before any child?
        #
        # TODO: input focus?
        cmd = super().handle(state_map['_self'], event)
        commands.extend(
            self.cmd_with_key('_self', None, c)
            for c in fhomm.command.aslist(cmd)
        )

        return commands

    def on_update(self, key, old, new):
        pass

    def handle_by_child(self, is_mouse_held, child, child_state, event):
        if Element.is_mouse_event(event):
            return self.handle_mouse_by_child(is_mouse_held, child, child_state, event)

        else:
            return child.element.handle(child_state, event)

    def handle_mouse_by_child(self, is_mouse_held, child, child_state, event):
        if is_mouse_held:
            should_handle = Element.is_mouse_held(child_state)

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
                child_state,
                Element.translate_mouse_event(event, child.relpos),
            )

    @staticmethod
    def cmd_with_key(int_key, ext_key, cmd):
        # print(f"cmd_with_key: {int_key} {ext_key} {cmd}")

        # it could already have a key in case of a direct update for another element
        if cmd.code == fhomm.command.UPDATE and 'key' not in cmd.kwargs:
            return fhomm.command.Command(
                fhomm.command.UPDATE,
                dict(cmd.kwargs, key=int_key),
            )

        elif cmd.code == fhomm.command.UPDATE_EXTERNAL:
            return fhomm.command.Command(
                fhomm.command.UPDATE,
                dict(cmd.kwargs, key=ext_key),
            )

        else:
            return cmd

    def make_return_value(self, state):
        pass
