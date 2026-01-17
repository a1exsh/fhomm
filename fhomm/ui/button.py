from collections import namedtuple

from fhomm.render import Pos
import fhomm.handler
import fhomm.render
import fhomm.ui


class ActiveArea(fhomm.ui.Element):

    # State = namedtuple('ActiveAreaState', ['is_pressed'], defaults=[False])

    def __init__(self, size, action, hotkey=None):
        super().__init__(size) #, ActiveArea.State)
        self.action = action
        self.hotkey = hotkey
        self.cmd_press = fhomm.handler.cmd_update(ActiveArea.set_pressed)
        self.cmd_release = fhomm.handler.cmd_update(ActiveArea.set_released)

    @classmethod
    def set_pressed(cls, _):
        # return ActiveArea.State(True)
        return {'is_pressed': True}

    @classmethod
    def set_released(cls, _):
        # return ActiveArea.State(False)
        return {'is_pressed': False}

    def on_key_down(self, state, key):
        if key == self.hotkey:
            return self.cmd_press

    def on_key_up(self, state, key):
        if key == self.hotkey and state['is_pressed']:
            return self.cmd_release, self.action()

    def on_mouse_down(self, state, pos, button):
        if button == 1:         # TODO: are there consts for this?
            return self.cmd_press

    def on_mouse_up(self, state, pos, button):
        if button == 1 and state['is_pressed']:
            return self.cmd_release, self.action()

    def on_mouse_leave(self, state):
        # FIXME: hold the hotkey, enter mouse, then leave => released
        return self.cmd_release

    # def on_window_closed(self, state):
    #     return self.cmd_release


class ActiveIcon(ActiveArea):
    def __init__(self, img, **kwargs):
        super().__init__(img.size, **kwargs)
        self.img = img

    def on_render(self, ctx, _):
        self.img.render(ctx)


class Button(ActiveIcon):
    def __init__(self, img, img_pressed, **kwargs):
        super().__init__(img, **kwargs)
        self.img_pressed = img_pressed

    def on_render(self, ctx, state):
        # print("on_render")
        img = self.img_pressed if state['is_pressed'] else self.img
        img.render(ctx)
