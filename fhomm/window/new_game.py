import pygame

import fhomm.ui
import fhomm.handler
from fhomm.render import Pos


class Handler(fhomm.ui.Window):
    def __init__(self, loader):
        super().__init__()
        self.bg_image = loader.load_image('newgame.bmp')
        self.measure(self.bg_image.dim)

    def on_render(self, ctx):
        self.bg_image.render(ctx)

    def on_event(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                return fhomm.handler.CMD_CLOSE
