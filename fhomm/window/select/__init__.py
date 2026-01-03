import pygame

from fhomm.render import Pos, Size
import fhomm.ui
import fhomm.handler


class ItemSelectorWindow(fhomm.ui.Window):
    def __init__(self, toolkit, title, items, item_size):
        super().__init__(border_width=16)

        font = toolkit.get_font()
        hl_font = toolkit.get_hl_font()
        self.bg_image = toolkit.load_image('request.bmp')
        self.measure(self.bg_image.size)

        self.attach(
            fhomm.ui.Label(Size(219, 20), font, title),
            Pos(50, 16),
        )

        # TODO: the two fonts could come from some form of a higher level UI toolkit
        img_list = fhomm.ui.ImgList(
            Size(206, 198),
            font,
            hl_font,
            items,
            item_size,
        )
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

    def on_render(self, ctx):
        self.bg_image.render(ctx)

    def cmd_cancel(self):
        return fhomm.handler.CMD_CLOSE
