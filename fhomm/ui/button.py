from collections import namedtuple

from fhomm.render import Pos
import fhomm.command
import fhomm.render
import fhomm.ui


def no_action(*args, **kwargs):
    pass


class ActiveArea(fhomm.ui.Element):

    class State(
        fhomm.ui.state_tuple(['is_pressed'], defaults=[False], submodule='button')
    ):
        @staticmethod
        def pressed(s):
            return s._replace(is_pressed=True)

        @staticmethod
        def released(s):
            return s._replace(is_pressed=False)

    CMD_PRESS = fhomm.command.cmd_update(State.pressed)
    CMD_RELEASE = fhomm.command.cmd_update(State.released)

    def __init__(
            self,
            rect,
            action=no_action,
            is_active=True,
            act_on_hold=False,
            hotkey=None,
            **kwargs
    ):
        super().__init__(rect, ActiveArea.State(is_active=is_active), **kwargs)
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

    def __init__(self, img, **kwargs):
        super().__init__(img.rect, **kwargs)
        self.img = img

    def on_render(self, ctx, _):
        if self.img is not None:
            self.img.render(ctx)


class DynamicIcon(ActiveArea):

    def __init__(self, rect, img_fn, **kwargs):
        super().__init__(rect, **kwargs)
        self.img_fn = img_fn

    def on_render(self, ctx, state, ext_state=None):
        if ext_state is not None:
            img = self.img_fn(state, ext_state)
        else:
            img = self.img_fn(state)

        if img is not None:
            img.render(ctx)


class Button(DynamicIcon):

    def __init__(self, img, img_pressed, **kwargs):
        def select_img(state, ext_state=None):
            if state.is_pressed or not state.is_active:
                return img_pressed

            else:
                return img

        super().__init__(img.rect, select_img, **kwargs)
