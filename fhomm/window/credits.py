import pygame

import fhomm.handler
import fhomm.ui


class CreditsScreen(fhomm.ui.Window):
    def __init__(self, toolkit):
        super().__init__(
            'credits',
            toolkit.load_image('credits.bmp'),
            border_width=0,
        )

    def on_mouse_up(self, _pos, _button):
        return fhomm.handler.CMD_CLOSE

    def on_key_up(self, _key):
        return fhomm.handler.CMD_CLOSE
