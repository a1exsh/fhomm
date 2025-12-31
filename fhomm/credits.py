import pygame

import fhomm.ui
import fhomm.handler
from fhomm.render import Pos, Dim, Rect


class Handler(fhomm.ui.Element): #ShadowCastingWindow
    def __init__(self, loader):
        super().__init__()
        self.image = loader.load_image('credits.bmp')
        self.measure(self.image.dim)

    def on_render(self, ctx):
        self.image.render(ctx)

    def on_event(self, event):
        if event.type == pygame.KEYUP:
            return fhomm.handler.CMD_CLOSE
