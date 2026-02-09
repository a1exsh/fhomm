from collections import namedtuple

import pygame

from fhomm.game.monsters import MONSTERS
from fhomm.render import Pos, Size, Rect
import fhomm.command
import fhomm.render
import fhomm.toolkit
import fhomm.ui
import fhomm.ui.button


class RecruitMonstersWindow(fhomm.ui.Window):
    def __init__(self, toolkit, monster):
        self.toolkit = toolkit
        self.monster = monster

        children = [
            fhomm.ui.Window.Slot(
                toolkit.label(
                    Size(280, 22),
                    f"Recruit {monster.name}", # TODO: make this translation-friendly
                ),
                Pos(179, 75),
                'lbl_title',
            ),
        ]

        super().__init__(
            toolkit.load_image('recruit.bmp'),
            children,
            border_width=16,
        )

    def on_key_up(self, key):
        if key == pygame.K_ESCAPE:
            return fhomm.command.CMD_CLOSE
