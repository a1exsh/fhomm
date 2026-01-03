import pygame

from fhomm.render import Pos, Size
import fhomm.handler
import fhomm.ui


class ItemSelectorWindow(fhomm.ui.Window):
    def __init__(self, toolkit, title, items, img_size):
        super().__init__(toolkit.load_image('request.bmp'), border_width=16)

        font = toolkit.get_font()
        hl_font = toolkit.get_hl_font()

        self.attach(toolkit.label(Size(219, 20), title), Pos(50, 16))

        img_list = toolkit.list(Size(206, 198), items, img_size)
        self.attach(img_list, Pos(56, 43))

        # OKAY
        self.attach(
            toolkit.button(
                'request.icn',
                1,
                action=self.cmd_cancel,
                hotkey=pygame.K_RETURN,
            ),
            Pos(36, 280),
        )

        # CANCEL
        self.attach(
            toolkit.button(
                'request.icn',
                3,
                action=self.cmd_cancel,
                hotkey=pygame.K_ESCAPE,
            ),
            Pos(189, 280),
        )

    def cmd_cancel(self):
        return fhomm.handler.CMD_CLOSE
