from collections import namedtuple

from fhomm.render import Pos
import fhomm.handler
import fhomm.render
import fhomm.ui


class State(namedtuple('State', ['is_pressed'], module='fhomm.ui.button')):
    __slots__ = ()

    @staticmethod
    def pressed(s):
        return s._replace(is_pressed=True)

    @staticmethod
    def released(s):
        return s._replace(is_pressed=False)


class ActiveArea(fhomm.ui.Element):

    CMD_PRESS = fhomm.handler.cmd_update(State.pressed)
    CMD_RELEASE = fhomm.handler.cmd_update(State.released)

    def __init__(self, size, action, hotkey=None):
        super().__init__(size, State(is_pressed=False))
        self.action = action
        self.hotkey = hotkey

    def on_key_down(self, key):
        if key == self.hotkey:
            return self.CMD_PRESS

    def on_key_up(self, key):
        # FIXME: don't leak state here, better handle it by tracking key/mouse "hold"
        if key == self.hotkey: # and state['is_pressed']:
            return self.CMD_RELEASE, self.action()

    def on_mouse_down(self, pos, button):
        if button == 1:         # TODO: are there consts for this?
            return self.CMD_PRESS

    def on_mouse_up(self, pos, button):
        if button == 1: # and state['is_pressed']:
            return self.CMD_RELEASE, self.action()

    def on_mouse_leave(self):
        # FIXME: hold the hotkey, enter mouse, then leave => released
        return self.CMD_RELEASE

    # def on_window_closed(self):
    #     return self.CMD_RELEASE


class ActiveIcon(ActiveArea):
    def __init__(self, img, **kwargs):
        super().__init__(img.size, **kwargs)
        self.img = img

    def on_render(self, ctx, _):
        self.img.render(ctx)


    def set_image(self, img):
        self.img = img


class Button(ActiveIcon):
    def __init__(self, img, img_pressed, **kwargs):
        super().__init__(img, **kwargs)
        self.img_pressed = img_pressed

    def on_render(self, ctx, state):
        # print("on_render")
        img = self.img_pressed if state.is_pressed else self.img
        img.render(ctx)
