import pygame

import fhomm.ui
import fhomm.handler


class Handler(fhomm.ui.Window):
    def __init__(self, loader):
        super().__init__(border_width=16)
        self.bg_image = loader.load_image('request.bmp')
        self.measure(self.bg_image.size)

    def on_render(self, ctx):
        self.bg_image.render(ctx)

    def on_key_up(self, key):
        if key == pygame.K_ESCAPE:
            return fhomm.handler.CMD_CLOSE
