import pygame

import fhomm.ui
import fhomm.handler
from fhomm.render import Pos, Dim


class Handler(fhomm.ui.Window):
    def __init__(self, loader):
        super().__init__(border_width=16)
        self.bg_image = loader.load_image('request.bmp')
        self.measure(self.bg_image.dim)

        # self.attach(
        #     fhomm.ui.IcnButton(loader, )
        # )

        self.hero_items = [
            fhomm.ui.ImgList.Item(
                loader.load_sprite('miniport.icn', i),
                "%04d".format(i),
            )
            for i in range(36)
        ]
        hero_list = fhomm.ui.ImgList(self.hero_items)
        hero_list.measure(Dim(206, 196))
        self.attach(hero_list, Pos(41, 28))

    def on_render(self, ctx):
        self.bg_image.render(ctx)

    def on_key_up(self, key):
        if key == pygame.K_ESCAPE: # TODO: handle via icn button
            return fhomm.handler.CMD_CLOSE
