from collections import namedtuple

import pygame

from fhomm.game.monsters import MONSTERS
from fhomm.render import Pos, Size, Rect
from fhomm.ui.window.view_army import ViewArmyWindow
import fhomm.command
import fhomm.render
import fhomm.ui
import fhomm.ui.button


class State(fhomm.ui.state_tuple(['monster_id'], submodule='recruit')):
    @property
    def monster_name(self):
        return MONSTERS[self.monster_id].name

    @staticmethod
    def next_monster(s):
        return s._replace(monster_id=((s.monster_id + 1) % len(MONSTERS)))

    @staticmethod
    def prev_monster(s):
        return s._replace(monster_id=((s.monster_id - 1) % len(MONSTERS)))


class RecruitMonstersWindow(fhomm.ui.Window):

    CMD_NEXT_MONSTER = fhomm.command.cmd_update(State.next_monster)
    CMD_PREV_MONSTER = fhomm.command.cmd_update(State.prev_monster)

    def __init__(self, toolkit, monster):
        self.toolkit = toolkit
        self.monster = monster

        children = [
            fhomm.ui.Window.Slot(
                toolkit.dynamic_label(
                    Size(286, 22),
                    # TODO: make this translation-friendly
                    lambda _, s: f"Recruit {s.monster_name}",
                ),
                Pos(17, 17),
                'lbl_title',
                '_self',
            ),
            fhomm.ui.Window.Slot(
                toolkit.dynamic_icon(
                    Size(68, 68),
                    lambda _, s: toolkit.load_sprite('monsters.icn', s.monster_id),
                    action=self.cmd_view_army,
                ),
                Pos(46, 46),
                'icn_monster',
                '_self',
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
            state=State(monster_id=monster.id),
        )

    def on_key_up(self, key):
        if key == pygame.K_ESCAPE:
            return fhomm.command.CMD_CLOSE

    def on_key_down(self, key):
        if key == pygame.K_RIGHT:
            return self.CMD_NEXT_MONSTER

        elif key == pygame.K_LEFT:
            return self.CMD_PREV_MONSTER

    def on_key_hold(self, key):
        return self.on_key_down(key)

    def cmd_view_army(self):
        return fhomm.command.cmd_show(
            ViewArmyWindow(self.toolkit, self.monster),
            Pos(100, 100),
            'view_army',
            casts_shadow=False,
        )
