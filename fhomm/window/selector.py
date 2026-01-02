import pygame

import fhomm.ui
import fhomm.handler
from fhomm.render import Pos, Dim


class Handler(fhomm.ui.Window):
    def __init__(self, loader, title, items, item_dim):
        super().__init__(border_width=16)

        font = loader.get_font()
        hl_font = loader.get_hl_font()
        self.bg_image = loader.load_image('request.bmp')
        self.measure(self.bg_image.dim)

        self.attach(
            fhomm.ui.Label(Dim(219, 20), font, title),
            Pos(50, 16),
        )

        # TODO: the two fonts could come from some form of a higher level UI toolkit
        img_list = fhomm.ui.ImgList(
            Dim(206, 198),
            font,
            hl_font,
            items,
            item_dim,
        )
        self.attach(img_list, Pos(56, 43))

        # OKAY
        self.attach(
            fhomm.ui.IcnButton(
                loader,
                'request.icn',
                1,
                self.cmd_cancel,
                pygame.K_RETURN,
            ),
            Pos(36, 280),
        )

        # CANCEL
        self.attach(
            fhomm.ui.IcnButton(
                loader,
                'request.icn',
                3,
                self.cmd_cancel,
                pygame.K_ESCAPE,
            ),
            Pos(189, 280),
        )

    def on_render(self, ctx):
        self.bg_image.render(ctx)

    def cmd_cancel(self):
        return fhomm.handler.CMD_CLOSE
