import pygame

import fhomm.ui
from fhomm.render import Pos
from fhomm.ui.button import AnimatedIcon


class ViewArmyWindow(fhomm.ui.Window):
    def __init__(self, toolkit, monster):
        self.toolkit = toolkit
        self.monster = monster

        children = [
            fhomm.ui.Window.Slot(
                toolkit.animated_icon(f'{monster.icn_name}.wlk', range(0, 6)),
                Pos(46, 46),
                'ani_monster_walk',
            ),
        ]

        super().__init__(
            toolkit.load_sprite('viewarmy.icn'),
            children,
            border_width=37,    # TODO: may need separate w/h here
        )

    def on_key_up(self, key):
        if key == pygame.K_ESCAPE:
            return fhomm.command.CMD_CLOSE
