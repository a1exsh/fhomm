import pygame

from fhomm.render import Pos, Size, Rect
import fhomm.handler
import fhomm.ui
import fhomm.ui.list


class ScrollBar(fhomm.ui.Element):

    def __init__(self, size, img_thumb):
        super().__init__(size, mouse_grab=True)

        self.img_thumb = img_thumb
        self.vrange = self.size.h - self.img_thumb.size.h - 6

    def on_render(self, ctx, state):
        self.img_thumb.render(ctx, Pos(3, 3 + int(state.scroll_degree * self.vrange)))

    def on_mouse_wheel(self, pos, dx, dy):
        return fhomm.handler.cmd_update(fhomm.ui.list.State.scroll_by(dy))

    def on_mouse_down(self, pos, button):
        if button == 1:
            return self.set_idx_from_pos(pos)

    def on_mouse_move(self, pos, rel, buttons):
        if buttons[0]:
            return self.set_idx_from_pos(pos)

    def set_idx_from_pos(self, pos):
        return fhomm.handler.cmd_update(
            fhomm.ui.list.State.scroll_to(
                (pos.y - self.img_thumb.size.h / 2) / self.vrange
            )
        )
