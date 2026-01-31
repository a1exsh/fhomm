from collections import namedtuple

from fhomm.render import Pos
import fhomm.command
import fhomm.render
import fhomm.ui


class State(
    namedtuple(
        'State',
        ['is_active', 'is_pressed'],
        defaults=[True, False],
        module='fhomm.ui.button',
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
    def pressed(s):
        return s._replace(is_pressed=True)

    @staticmethod
    def released(s):
        return s._replace(is_pressed=False)


class ActiveArea(fhomm.ui.Element):

    CMD_PRESS = fhomm.command.cmd_update(State.pressed)
    CMD_RELEASE = fhomm.command.cmd_update(State.released)

    def __init__(self, size, action, act_on_hold=False, hotkey=None, **kwargs):
        super().__init__(size, State(**kwargs))
        self.action = action
        self.act_on_hold = act_on_hold
        self.hotkey = hotkey

    def on_key_down(self, key):
        if key == self.hotkey:
            return self.CMD_PRESS

    def on_key_up(self, key):
        # FIXME: don't leak state here, better handle it by tracking key/mouse "hold"
        if key == self.hotkey: # and state['is_pressed']:
            return self.CMD_RELEASE, self.action()

    def on_mouse_down(self, pos, button):
        if button == 1:         # TODO: are there consts for mouse buttons: L/M/R?
            if self.act_on_hold:
                return self.CMD_PRESS, self.action()
            else:
                return self.CMD_PRESS

    def on_mouse_hold(self, button):
        # TODO: what about hotkey hold?
        if button == 1:
            if self.act_on_hold:
                return self.action()

    def on_mouse_up(self, pos, button):
        # FIXME: we don't have access to state here, but shouldn't trigger action if it wasn't pressed...
        if button == 1:
            if self.act_on_hold:
                return self.CMD_RELEASE
            else:
                return self.CMD_RELEASE, self.action()

    def on_mouse_leave(self):
        # FIXME: hold the hotkey, enter mouse, then leave => released
        return self.CMD_RELEASE


class ActiveIcon(ActiveArea):
    def __init__(self, img, **kwargs):
        super().__init__(img.size, **kwargs)
        self.img = img

    def on_render(self, ctx, _):
        self.img.render(ctx)

    # TODO: move to the state
    def set_image(self, img):
        self.img = img


class Button(ActiveIcon):
    def __init__(self, img, img_pressed, **kwargs):
        super().__init__(img, **kwargs)
        self.img_pressed = img_pressed

    def on_render(self, ctx, state):
        # TODO: is_active should be part of the state, right?
        img = self.img_pressed if state.is_pressed or not state.is_active else self.img
        img.render(ctx)
