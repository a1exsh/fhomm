import pygame

import fhomm.ui
import fhomm.handler
from fhomm.render import Pos, Dim


class Handler(fhomm.ui.Window):
    def __init__(self, loader):
        super().__init__(border_width=16)
        self.bg_image = loader.load_image('request.bmp')
        self.measure(self.bg_image.dim)

        self.hero_items = [
            fhomm.ui.ImgList.Item(
                loader.load_sprite('miniport.icn', i),
                "%04d".format(i),
            )
            for i in range(36)
        ]
        bg_item = loader.load_sprite('locators.icn', 21)
        hero_list = fhomm.ui.ImgList(self.hero_items, bg_item)
        hero_list.measure(Dim(206, 196))
        self.attach(hero_list, Pos(41, 28))

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
