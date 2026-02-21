from collections import namedtuple

import pygame

from fhomm.game.monsters import MONSTERS
from fhomm.render import Pos, Size, Rect
from fhomm.ui.window.view_army import ViewArmyWindow
import fhomm.command
import fhomm.render
import fhomm.ui
import fhomm.ui.button


class RecruitMonstersWindow(fhomm.ui.Window):
    def __init__(self, toolkit, monster):
        self.toolkit = toolkit
        self.monster = monster

        children = [
            fhomm.ui.Window.Slot(
                toolkit.label(
                    Size(286, 22),
                    f"Recruit {monster.name}", # TODO: make this translation-friendly
                ),
                Pos(17, 17),
                'lbl_title',
            ),
            fhomm.ui.Window.Slot(
                toolkit.icon(
                    'monsters.icn',
                    monster.id,
                    action=self.cmd_view_army,
                ),
                Pos(46, 46),
                'icn_monster',
            ),
            fhomm.ui.Window.Slot(
                toolkit.label(
                    Size(120, 10),
                    f"Number to buy:",
                    font=toolkit.get_small_font(),
                ),
                Pos(17, 150),
                'lbl_number',
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

    def cmd_view_army(self):
        return fhomm.command.cmd_show(
            ViewArmyWindow(self.toolkit, self.monster),
            Pos(100, 100),
            'view_army',
            casts_shadow=False,
        )
