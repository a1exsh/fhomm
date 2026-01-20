import pygame

import fhomm.handler
import fhomm.ui


class LoadGameMenu(fhomm.ui.Window):
    # standard, campaign, multiplayer
    def __init__(self, loader):
        super().__init__(
            loader.load_image('request.bmp'),
            border_width=16,
        )

    def on_key_up(self, key):
        if key == pygame.K_ESCAPE:
            return fhomm.handler.CMD_CLOSE
