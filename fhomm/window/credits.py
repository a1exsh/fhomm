import pygame

import fhomm.ui
import fhomm.handler


# could also be done as a window for than default higher resolutions
class CreditsScreen(fhomm.ui.Element):
    def __init__(self, toolkit):
        super().__init__()
        self.image = toolkit.load_image('credits.bmp')
        self.measure(self.image.size)

    def on_render(self, ctx):
        self.image.render(ctx)

    def on_mouse_up(self, pos, button):
        return fhomm.handler.CMD_CLOSE

    def on_key_up(self, _key):
        return fhomm.handler.CMD_CLOSE
