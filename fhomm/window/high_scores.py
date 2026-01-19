import pygame

import fhomm.handler
import fhomm.ui


class HighScoresWindow(fhomm.ui.Window):
    def __init__(self, toolkit):
        super().__init__(toolkit.load_image('hiscore.bmp'))

    # TODO: use the actual buttons
    def on_key_up(self, key):
        if key == pygame.K_ESCAPE:
            return fhomm.handler.CMD_CLOSE
