import pygame

from fhomm.render import Pos, Size, Rect
import fhomm.command
import fhomm.ui
import fhomm.ui.list


class ScrollBar(fhomm.ui.Element):

    def __init__(self, rect, img_thumb, pad=Size(3, 3)):
        super().__init__(rect, grabs_mouse=True)

        self.img_thumb = img_thumb
        self.pad = pad
        self.vrange = self.rect.h - self.img_thumb.size.h - 6

    # could have a pressed internal state with a pressed thumb image
    def on_render(self, ctx, _, lst_state):
        self.img_thumb.render(
            ctx,
            Pos(self.pad.w, self.pad.h + int(lst_state.scroll_degree * self.vrange)),
        )

    def on_mouse_wheel(self, pos, dx, dy):
        return fhomm.command.cmd_update(fhomm.ui.list.State.scroll_by(dy))

    def on_mouse_down(self, pos, button):
        if button == 1:
            return self.set_degree_from_pos(pos)

    def on_mouse_move(self, pos, rel, buttons):
        if buttons[0]:
            return self.set_degree_from_pos(pos)

    def set_degree_from_pos(self, pos):
        return fhomm.command.cmd_update_external(
            fhomm.ui.list.State.scroll_to(
                (pos.y - self.pad.h - self.img_thumb.size.h / 2) / self.vrange
            )
        )
