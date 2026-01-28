import pygame

from fhomm.render import Pos, Size
import fhomm.handler
import fhomm.ui
import fhomm.ui.list


class ItemSelectorWindow(fhomm.ui.Window):
    def __init__(self, toolkit, title, items, img_size, return_key):
        self.return_key = return_key

        font = toolkit.get_font()
        hl_font = toolkit.get_hl_font()

        item_list = toolkit.list(Size(208, 200), items, img_size)

        # add scroll up/down buttons that react to mouse hold
        children = [
            fhomm.ui.Window.Slot(
                toolkit.label(Size(219, 20), title),
                Pos(50, 16),
                'lbl_title',
            ),
            fhomm.ui.Window.Slot(item_list, Pos(56, 41), 'lst_items'),
            fhomm.ui.Window.Slot(
                toolkit.button(
                    'scroll.icn',
                    0,
                    action=self.cmd_scroll_up,
                    act_on_hold=True,
                ),
                Pos(280, 37),
                'btn_scroll_up',
            ),
            fhomm.ui.Window.Slot(
                toolkit.scrollbar(Size(8, 173)),
                Pos(283, 56),
                'lst_items',
            ),
            fhomm.ui.Window.Slot(
                toolkit.button(
                    'scroll.icn',
                    2,
                    action=self.cmd_scroll_down,
                    act_on_hold=True,
                ),
                Pos(280, 234),
                'btn_scroll_down',
            ),
            fhomm.ui.Window.Slot(
                toolkit.dynamic_label(
                    Size(225, 16),
                    lambda s: (s.selected_item.text if s.selected_item else None),
                ),
                Pos(48, 254),
                'lst_items',
            ),
            fhomm.ui.Window.Slot(
                toolkit.button(
                    'request.icn',
                    1,
                    action=self.cmd_return,
                    hotkey=pygame.K_RETURN,
                ),
                Pos(36, 280),
                'btn_okay',
            ),
            fhomm.ui.Window.Slot(
                toolkit.button(
                    'request.icn',
                    3,
                    action=self.cmd_cancel,
                    hotkey=pygame.K_ESCAPE,
                ),
                Pos(189, 280),
                'btn_cancel',
            ),
        ]

        super().__init__(
            toolkit.load_image('request.bmp'),
            children,
            border_width=16,
        )

    def make_return_value(self, state):
        return state['lst_items'].selected_idx

    def cmd_scroll_up(self):
        return fhomm.handler.cmd_update_other(
            'lst_items',
            fhomm.ui.list.State.scroll_by(-1),
        )

    def cmd_scroll_down(self):
        return fhomm.handler.cmd_update_other(
            'lst_items',
            fhomm.ui.list.State.scroll_by(1),
        )

    def cmd_return(self):
        return fhomm.handler.cmd_close(self.return_key)

    def cmd_cancel(self):
        return fhomm.handler.CMD_CLOSE
