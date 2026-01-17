import pygame

import fhomm.handler
import fhomm.ui


class HighScoresWindow(fhomm.ui.Window):
    def __init__(self, toolkit):
        super().__init__(
            'high_scores',
            toolkit.load_image('hiscore.bmp'),
            border_width=0,
        )

    # TODO: use the actual buttons
    def on_key_up(self, key):
        if key == pygame.K_ESCAPE:
            return fhomm.handler.CMD_CLOSE
