import pygame

import fhomm.ui
import fhomm.handler
from fhomm.render import Pos, Dim


class Handler(fhomm.ui.Window):
    def __init__(self, loader, title, items, item_dim):
        super().__init__(border_width=16)

        self.font = loader.get_big_font()
        self.bg_image = loader.load_image('request.bmp')
        self.measure(self.bg_image.dim)

        self.attach(
            fhomm.ui.Label(Dim(219, 20), self.font, title),
            Pos(34, 0),
        )

        img_list = fhomm.ui.ImgList(
            Dim(206, 198),
            loader.get_big_font(),
            items,
            item_dim,
        )
        self.attach(img_list, Pos(40, 27))

        # OKAY
        self.attach(
            fhomm.ui.IcnButton(
                loader,
                'request.icn',
                1,
                self.cmd_cancel,
                pygame.K_RETURN,
            ),
            Pos(20, 264),
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
            Pos(173, 264),
        )

    def on_render(self, ctx):
        self.bg_image.render(ctx)

    def cmd_cancel(self):
        return fhomm.handler.CMD_CLOSE
