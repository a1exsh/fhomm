import pygame

from fhomm.render import Pos, Size, Rect
import fhomm.handler
import fhomm.ui


class ScrollBar(fhomm.ui.Element):

    def __init__(self, size, img_thumb):
        super().__init__(size)

        self.img_thumb = img_thumb

    def on_render(self, ctx, state):
        max_scroll_idx = 28
        vrange = self.size.h - self.img_thumb.size.h

        scroll_idx = state.get('scroll_idx', 0)
        posy = scroll_idx / max_scroll_idx * vrange
        # print(f"vrange={vrange} posy={posy}")

        self.img_thumb.render(ctx, Pos(0, int(posy)))

    def on_mouse_wheel(self, pos, dx, dy):
        # self.scroll_by(dy)
        return fhomm.handler.cmd_update(
            lambda s: dict(s, scroll_idx=(s.get('scroll_idx', 0) + dy))
        )

    def on_mouse_down(self, pos, button):
        if button == 1:
            return self.set_idx_from_pos(pos)

    def on_mouse_move(self, pos, rel, buttons):
        if buttons[0]:
            return self.set_idx_from_pos(pos)

    def set_idx_from_pos(self, pos):
        max_scroll_idx = 28
        vrange = self.size.h - self.img_thumb.size.h

        scroll_idx = max(
            0,
            min(
                int((pos.y - self.img_thumb.size.h/2) / vrange * max_scroll_idx),
                max_scroll_idx,
            ),
        )

        return fhomm.handler.cmd_update(
            lambda s: dict(s, scroll_idx=scroll_idx)
        )
