from collections import namedtuple

import pygame

from fhomm.render import Pos, Size, Rect
import fhomm.ui

Item = namedtuple('Item', ['img', 'text'], module='fhomm.ui.list')


class List(fhomm.ui.Element):

    def __init__(
            self,
            size,
            font,
            hl_font,
            items,
            img_size,
            item_vpad=1,
            text_hpad=4
    ):
        super().__init__()
        self.measure(size)

        self.font = font
        self.hl_font = hl_font

        self.img_size = img_size
        self.item_vpad = item_vpad
        self.text_hpad = text_hpad

        self.items = items

        self.selected_idx = None
        self.scroll_idx = 0
        self.items_per_page = size.h // (img_size.h + item_vpad)

        self.list_pad = Size(
            3,
            (size.h - self.items_per_page*(img_size.h + item_vpad)) // 2,
        )

        self._bg_capture = None

        self.tick = 0
        self.key_hold_ticks = 50
        self.key_hold_delta = None

    def on_render(self, ctx):
        if self._bg_capture is None:
            self._bg_capture = ctx.capture(self.rect)
        else:
            self._bg_capture.render(ctx)

        for i in range(min(len(self.items), self.items_per_page)):
            item_idx = self.scroll_idx + i
            item = self.items[item_idx]

            img_pos = Pos(
                self.list_pad.w,
                self.list_pad.h + (self.img_size.h + self.item_vpad)*i,
            )
            if item.img:
                item.img.render(ctx, img_pos)

            if item.text:
                text_pos = Pos(
                    img_pos.x + self.img_size.w + self.text_hpad,
                    img_pos.y,
                )
                self.render_item_text(
                    ctx,
                    item.text,
                    text_pos,
                    item_idx == self.selected_idx,
                )

    def render_item_text(self, ctx, text, text_pos, is_selected):
        bound_rect = Rect.of(
            Size(self.rect.right - text_pos.x, self.img_size.h),
            text_pos,
        )
        if fhomm.ui.DEBUG_RENDER:
            ctx.draw_rect(240, bound_rect, width=1)

        font = self.hl_font if is_selected else self.font
        text_size = font.measure_multiline_text(text, bound_rect)

        # center vertically before actually drawing the item text
        text_rect = Rect.of(
            text_size,
            Pos(
                text_pos.x,
                text_pos.y + (self.img_size.h - text_size.h) // 2,
            ),
        )
        if fhomm.ui.DEBUG_RENDER:
            ctx.draw_rect(224, text_rect, width=1)

        font.draw_multiline_text(ctx, text, text_rect)

    def set_scroll_idx(self, idx):
        old, self.scroll_idx = self.scroll_idx, idx
        if old != self.scroll_idx:
            self.dirty()

    def get_max_scroll_idx(self):
        return max(0, len(self.items) - self.items_per_page)

    def scroll_by(self, delta):
        self.set_scroll_idx(
            max(0, min(self.scroll_idx + delta, self.get_max_scroll_idx()))
        )

    def set_selected_idx(self, idx):
        old, self.selected_idx = self.selected_idx, idx
        if old != self.selected_idx:
            self.dirty()

    def move_selection_by(self, delta):
        self.set_selected_idx(
            max(0, min(self.selected_idx + delta, len(self.items) - 1))
        )
        if self.selected_idx < self.scroll_idx:
            self.set_scroll_idx(self.selected_idx)

        elif self.selected_idx >= self.scroll_idx + self.items_per_page:
            self.set_scroll_idx(self.selected_idx - self.items_per_page + 1)

    def on_key_down(self, key):
        if not self.items:      # no selection in an empty list
            return

        delta = None

        if key == pygame.K_UP:
            delta = -1

        elif key == pygame.K_DOWN:
            delta = 1

        elif key == pygame.K_PAGEUP:
            delta = -self.items_per_page

        elif key == pygame.K_PAGEDOWN:
            delta = self.items_per_page

        elif key == pygame.K_HOME:
            self.set_selected_idx(0)
            self.set_scroll_idx(0)

        elif key == pygame.K_END:
            self.set_selected_idx(len(self.items) - 1)
            self.set_scroll_idx(self.get_max_scroll_idx())

        if delta is not None and self.key_hold_delta is None:
            if self.selected_idx is None:
                self.set_selected_idx(0)
            else:
                self.move_selection_by(delta)

            self.tick = -250    # start repeating after a short delay 
            self.key_hold_delta = delta

    def on_key_up(self, key):
        if key in [pygame.K_DOWN, pygame.K_UP, pygame.K_PAGEDOWN, pygame.K_PAGEUP]:
            self.key_hold_delta = None

    def on_tick(self, dt):
        if self.key_hold_delta is not None:
            self.tick += dt
            while self.tick >= self.key_hold_ticks:
                self.move_selection_by(self.key_hold_delta)
                self.tick -= self.key_hold_ticks

    def on_mouse_down(self, pos, button):
        if button == 1:
            visible_idx = (
                (pos.y - self.list_pad.h)
                //
                (self.img_size.h + self.item_vpad)
            )
            item_idx = self.scroll_idx + visible_idx
            last_visible_idx = min(
                self.scroll_idx + self.items_per_page,
                len(self.items),
            )
            if item_idx in range(last_visible_idx):
                self.set_selected_idx(item_idx)

    def on_mouse_wheel(self, pos, dx, dy):
        self.scroll_by(dy)
