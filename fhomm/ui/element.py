from fhomm.render import Pos
import fhomm.ui


class Label(fhomm.ui.Element):
    def __init__(self, size, font, text):
        super().__init__()
        self.measure(size)
        self.font = font
        self.text = text

        text_size = font.measure_text(text)
        self.text_pos = Pos(
            (size.w - text_size.w) // 2,
            (size.h - text_size.h) // 2,
        )

    def on_render(self, ctx):
        self.font.draw_text(ctx, self.text, self.text_pos)


class ActiveArea(fhomm.ui.Element):
    def __init__(self, action, hotkey=None):
        super().__init__()
        self.action = action
        self.hotkey = hotkey

        self.is_pressed = False

    def set_pressed(self):
        old, self.is_pressed = self.is_pressed, True
        return old != self.is_pressed

    def set_released(self):
        old, self.is_pressed = self.is_pressed, False
        return old != self.is_pressed

    def press(self):
        if self.set_pressed():
            self.dirty()

    def release(self, action=True):
        if self.set_released():
            self.dirty()
            if action:
                return self.action()

    def on_key_down(self, key):
        if key == self.hotkey:
            return self.press()

    def on_key_up(self, key):
        if key == self.hotkey:
            return self.release()

    def on_mouse_leave(self):
        # FIXME: hold the hotkey, enter mouse, then leave => released
        self.release(action=False)

    def on_mouse_down(self, pos, button):
        # print(f"{self} mouse down: {pos} {button}")
        if button == 1:         # TODO: are there consts for this?
            return self.press()

    def on_mouse_up(self, pos, button):
        if button == 1:
            return self.release()


class ActiveIcon(ActiveArea):
    def __init__(self, img, **kwargs):
        super().__init__(**kwargs)
        self.img = img
        self.measure(self.img.size)

    def on_render(self, ctx):
        self.img.render(ctx)


class Button(ActiveIcon):
    def __init__(self, img, img_pressed, **kwargs):
        super().__init__(img, **kwargs)
        self.img_pressed = img_pressed

    def on_render(self, ctx):
        img = self.img_pressed if self.is_pressed else self.img
        img.render(ctx)
