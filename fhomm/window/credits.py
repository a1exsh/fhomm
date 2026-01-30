import pygame

import fhomm.command
import fhomm.ui


class CreditsScreen(fhomm.ui.Window):
    def __init__(self, toolkit):
        super().__init__(toolkit.load_image('credits.bmp'))

    def on_mouse_up(self, _pos, _button):
        return fhomm.command.CMD_CLOSE

    def on_key_up(self, _key):
        return fhomm.command.CMD_CLOSE
