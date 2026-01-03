import pygame

import fhomm.ui
import fhomm.handler


class HighScoresWindow(fhomm.ui.Window):
    def __init__(self, toolkit):
        super().__init__(border_width=0)
        self.image = toolkit.load_image('hiscore.bmp')
        self.measure(self.image.size)

    def on_render(self, ctx):
        self.image.render(ctx)

    # TODO: use the actual buttons
    def on_key_up(self, key):
        if key == pygame.K_ESCAPE:
            return fhomm.handler.CMD_CLOSE
