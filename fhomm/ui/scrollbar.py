import pygame

from fhomm.render import Pos, Size, Rect
import fhomm.ui


class ScrollBar(fhomm.ui.Element):

    def __init__(self, size, img_thumb):
        super().__init__(size)

        self.img_thumb = img_thumb

    def on_render(self, ctx, state):
        max_scroll_idx = 28

        scroll_idx = state.get('scroll_idx', 0)
        vrange = self.size.h - self.img_thumb.size.h
        posy = scroll_idx / max_scroll_idx * vrange
        # print(f"vrange={vrange} posy={posy}")

        self.img_thumb.render(ctx, Pos(0, int(posy)))
