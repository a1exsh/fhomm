from collections import namedtuple

from fhomm.render import Pos
import fhomm.command
import fhomm.render
import fhomm.ui


def state_tuple(fields=[], defaults=[], submodule='', **kwargs):

    class State(
        fhomm.ui.state_tuple(
            fields + ['is_pressed'],
            defaults=(defaults + [False]),
            submodule=('button.' + submodule),
            **kwargs
        )
    ):
        @staticmethod
        def pressed(s):
            return s._replace(is_pressed=True)

        @staticmethod
        def released(s):
            return s._replace(is_pressed=False)

    return State


class ActiveArea(fhomm.ui.Element):

    State = state_tuple(submodule='ActiveArea')

    CMD_PRESS = fhomm.command.cmd_update(State.pressed)
    CMD_RELEASE = fhomm.command.cmd_update(State.released)

    def __init__(
            self,
            size,
            state,
            action,
            act_on_hold=False,
            hotkey=None,
            **kwargs
    ):
        super().__init__(size, state, **kwargs)
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


class Icon(ActiveArea):

    class State(state_tuple(['img'], submodule='Icon')):
        @staticmethod
        def set_image(img):
            return lambda s: s._replace(img=img)

    def __init__(self, state, **kwargs):
        super().__init__(state.img.size, state, **kwargs)

    def on_render(self, ctx, state):
        if state.img is not None:
            state.img.render(ctx)


class Button(Icon):

    State = state_tuple(['img', 'img_pressed'], submodule='Button')

    def __init__(self, img, img_pressed, is_active=True, **kwargs):
        super().__init__(Button.State(img, img_pressed, is_active=is_active), **kwargs)
        self.img_pressed = img_pressed

    def on_render(self, ctx, state):
        if state.is_pressed or not state.is_active:
            img = state.img_pressed

        else:
            img = state.img

        img.render(ctx)
