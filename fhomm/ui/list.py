from collections import namedtuple

import pygame

from fhomm.render import Pos, Size, Rect
import fhomm.ui


class Item(namedtuple('Item', ['img', 'text'], module='fhomm.ui.list')):
    __slots__ = ()

    def __getstate__(self):
        return self._asdict()

    def __getnewargs__(self):
        return ()


class State(
    namedtuple(
        'State',
        [
            'items',
            'num_items_per_page',
            'selected_idx',
            'scroll_idx'
        ],
        module='fhomm.ui.list',
    )
):
    __slots__ = ()

    # def __getstate__(self):
    #     return dict(
    #         self._asdict(),
    #         items=[itm.text for itm in self.items],
    #     )

    def __getnewargs__(self):
        return ()

    @property
    def selected_item(self):
        if self.selected_idx is not None:
            return self.items[self.selected_idx]

    @property
    def max_scroll_idx(self):
        return max(0, len(self.items) - self.num_items_per_page)

    def clamp_item_idx(self, idx):
        return max(0, min(idx, len(self.items) - 1))

    def clamp_scroll_idx(self, idx):
        return max(0, min(idx, self.max_scroll_idx))

    def clamp_on_page_idx(self, idx):
        return max(0, min(idx, self.num_items_per_page - 1))

    # @staticmethod
    # def scroll_to(idx):
    #     return lambda s: s._replace(scroll_idx=s.clamp_scroll_idx(idx))

    @property
    def scroll_degree(self):
        return self.scroll_idx / self.max_scroll_idx # FIXME: dividing by 0, huh?

    @staticmethod
    def scroll_to(degree):
        return lambda s: s._replace(
            scroll_idx=s.clamp_scroll_idx(int(degree * s.max_scroll_idx))
        )

    @staticmethod
    def scroll_by(rel_idx):
        return lambda s: s._replace(
            scroll_idx=s.clamp_scroll_idx(s.scroll_idx + rel_idx)
        )

    @staticmethod
    def select_first(s):
        if len(s.items) > 0:
            return s._replace(selected_idx=0, scroll_idx=0)

        else:
            return s

    @staticmethod
    def select_last(s):
        if len(s.items) > 0:
            return s._replace(
                selected_idx=(len(s.items) - 1),
                scroll_idx=s.max_scroll_idx,
            )

        else:
            return s

    @staticmethod
    def scroll_to_selected(s):
        if s.selected_idx < s.scroll_idx:
            return s._replace(scroll_idx=s.selected_idx)

        elif s.selected_idx >= s.scroll_idx + s.num_items_per_page:
            return s._replace(scroll_idx=(s.selected_idx - s.num_items_per_page + 1))

        else:
            return s

    @staticmethod
    def select_prev(s):
        if len(s.items) > 0:
            return State.scroll_to_selected(
                s._replace(selected_idx=s.clamp_item_idx((s.selected_idx or 0) - 1))
            )

        else:
            return s

    @staticmethod
    def select_next(s):
        if len(s.items) > 0:
            if s.selected_idx is None: # no selection is a special case here
                next_idx = 0
            else:
                next_idx = s.clamp_item_idx(s.selected_idx + 1)

            return State.scroll_to_selected(s._replace(selected_idx=next_idx))

        else:
            return s

    @staticmethod
    def select_prev_page(s):
        if len(s.items) > 0:
            return State.scroll_to_selected(
                s._replace(
                    selected_idx=s.clamp_item_idx(
                        (s.selected_idx or 0) - s.num_items_per_page
                    )
                )
            )

        else:
            return s

    @staticmethod
    def select_next_page(s):
        if len(s.items) > 0:
            return State.scroll_to_selected(
                s._replace(
                    selected_idx=s.clamp_item_idx(
                        (s.selected_idx or 0) + s.num_items_per_page
                    )
                )
            )

        else:
            return s

    @staticmethod
    def select_at(idx_on_page):
        def select(s):
            if len(s.items) > 0:
                return s._replace(
                    selected_idx=max(
                        0,
                        min(
                            s.scroll_idx + s.clamp_on_page_idx(idx_on_page),
                            len(s.items) - 1
                        )
                    )
                )

            else:
                return s

        return select


class List(fhomm.ui.Element):

    def __init__(
            self,
            size,
            font,
            hl_font,
            items,
            img_size,
            item_vpad=1,
            text_hpad=4,
    ):
        self.font = font
        self.hl_font = hl_font

        self.img_size = img_size
        self.item_vpad = item_vpad
        self.text_hpad = text_hpad

        num_items_per_page = size.h // (img_size.h + item_vpad)
        self.list_pad = Size(
            3,
            (
                size.h
                - num_items_per_page * img_size.h
                - max(0, num_items_per_page - 1) * item_vpad
            ) // 2,
        )

        super().__init__(
            size,
            fhomm.ui.list.State(
                items=items,
                num_items_per_page=num_items_per_page,
                scroll_idx=0,
                selected_idx=None,
            )
        )

        self._bg_capture = None

        # TODO: generalize as key hold event
        self.tick = 0
        self.key_hold_ticks = 50
        self.key_hold_delta = None

    def on_render(self, ctx, state):
        if self._bg_capture is None:
            self._bg_capture = ctx.capture(self.rect)
        else:
            self._bg_capture.render(ctx)

        for i in range(min(len(state.items), state.num_items_per_page)):
            item_idx = state.scroll_idx + i
            item = state.items[item_idx]

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
                    item_idx == state.selected_idx,
                )

    def render_item_text(self, ctx, text, text_pos, is_selected):
        text_rect = Rect.of(
            Size(self.rect.right - text_pos.x + 1, self.img_size.h),
            text_pos,
        )
        if fhomm.ui.DEBUG_RENDER:
            ctx.draw_rect(240, text_rect, width=1)

        font = self.hl_font if is_selected else self.font

        # if fhomm.ui.DEBUG_RENDER:
        #     ctx.draw_rect(224, text_rect, width=1)

        font.draw_multiline_text(
            ctx,
            text,
            text_rect,
            valign=fhomm.render.CENTER,
        )

    def on_key_down(self, key):
        if key == pygame.K_HOME:
            return fhomm.handler.cmd_update(State.select_first)

        elif key == pygame.K_END:
            return fhomm.handler.cmd_update(State.select_last)

        elif key == pygame.K_UP:
            return fhomm.handler.cmd_update(State.select_prev)

        elif key == pygame.K_DOWN:
            return fhomm.handler.cmd_update(State.select_next)

        elif key == pygame.K_PAGEUP:
            return fhomm.handler.cmd_update(State.select_prev_page)

        elif key == pygame.K_PAGEDOWN:
            return fhomm.handler.cmd_update(State.select_next_page)

    def on_key_hold(self, key):
        return self.on_key_down(key)

    def on_mouse_down(self, pos, button):
        if button == 1:
            idx_on_page = (
                (pos.y - self.list_pad.h)
                //
                (self.img_size.h + self.item_vpad)
            )
            return fhomm.handler.cmd_update(State.select_at(idx_on_page))

    def on_mouse_wheel(self, pos, dx, dy):
        return fhomm.handler.cmd_update(State.scroll_by(dy))
