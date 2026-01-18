import pygame

from fhomm.render import Pos, Size
import fhomm.handler
import fhomm.ui


class ItemSelectorWindow(fhomm.ui.Window):
    def __init__(self, state_key, toolkit, title, items, img_size):
        super().__init__(
            state_key,
            toolkit.load_image('request.bmp'),
            border_width=16,
        )

        font = toolkit.get_font()
        hl_font = toolkit.get_hl_font()

        self.attach(toolkit.label(Size(219, 20), title), Pos(50, 16))

        item_list = toolkit.list(Size(206, 198), items, img_size)
        self.attach(item_list, Pos(56, 43), 'item_list')

        self.attach(
            toolkit.scrollbar(Size(8, 173)),
            Pos(283, 56),
            'item_list',
        )

        label_selected_item = toolkit.dynamic_label(
            Size(225, 19),
            lambda s: str(s.get('selected_idx') or ''),
        )
        self.attach(label_selected_item, Pos(48, 253), 'item_list')

        btn_okay = toolkit.button(
            'request.icn',
            1,
            action=self.cmd_cancel,
            hotkey=pygame.K_RETURN,
        )
        self.attach(btn_okay, Pos(36, 280), 'btn_okay')

        btn_cancel = toolkit.button(
            'request.icn', 3, action=self.cmd_cancel, hotkey=pygame.K_ESCAPE
        )
        self.attach(btn_cancel, Pos(189, 280), 'btn_cancel')

        # TODO: move to Window ctor, build from children list
        self.initial_state_map = {
            'item_list': item_list.initial_state,
            'btn_okay': btn_okay.initial_state,
            'btn_cancel': btn_cancel.initial_state,
        }

    def cmd_cancel(self):
        return fhomm.handler.CMD_CLOSE
