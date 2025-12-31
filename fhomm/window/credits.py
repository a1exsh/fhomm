import pygame

import fhomm.ui
import fhomm.handler


class Handler(fhomm.ui.Element): #ShadowCastingWindow
    def __init__(self, loader):
        super().__init__()
        self.image = loader.load_image('credits.bmp')
        self.measure(self.image.dim)

    def on_render(self, ctx):
        self.image.render(ctx)

    def on_mouse_up(self, pos, button):
        return fhomm.handler.CMD_CLOSE

    def on_key_up(self, _key):
        return fhomm.handler.CMD_CLOSE
