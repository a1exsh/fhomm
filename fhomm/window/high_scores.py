import pygame

import fhomm.ui
import fhomm.handler


class Handler(fhomm.ui.Window):
    def __init__(self, loader):
        super().__init__(border_width=0)
        self.image = loader.load_image('hiscore.bmp')
        self.measure(self.image.dim)

    def on_render(self, ctx):
        self.image.render(ctx)

    def on_key_up(self, key):
        if key == pygame.K_ESCAPE:
            return fhomm.handler.CMD_CLOSE
