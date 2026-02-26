import pygame

import fhomm.ui
from fhomm.game.monsters import MONSTERS, WIP_ICN_MONSTERS
from fhomm.render import Pos
from fhomm.ui.button import AnimatedIcon


class State(fhomm.ui.state_tuple(['monster_id'], submodule='view_army')):
    @property
    def monster(self):
        return MONSTERS[self.monster_id]

    @staticmethod
    def next_monster(s):
        return s._replace(monster_id=((s.monster_id + 1) % len(MONSTERS)))

    @staticmethod
    def prev_monster(s):
        return s._replace(monster_id=((s.monster_id - 1) % len(MONSTERS)))


class ViewArmyWindow(fhomm.ui.Window):

    CMD_NEXT_MONSTER = fhomm.command.cmd_update(State.next_monster)
    CMD_PREV_MONSTER = fhomm.command.cmd_update(State.prev_monster)

    def __init__(self, toolkit, monster):

        all_monster_imgs = [
            toolkit.load_sprite(icn, idx)
            for icn in [self.icn_name(m.icn_name) for m in MONSTERS]
            for idx in range(0, 6)
        ]
        min_off_x = min(img.offset.x for img in all_monster_imgs)
        min_off_y = min(img.offset.y for img in all_monster_imgs)
        imgs = [
            img.moved_by(fhomm.render.Pos(-min_off_x, -min_off_y))
            for img in all_monster_imgs
        ]

        children = [
            fhomm.ui.Window.Slot(
                fhomm.ui.button.AnimatedIcon(imgs),
                Pos(46, 46),
                'ani_monster_walk',
            ),
        ]

        super().__init__(
            toolkit.load_sprite('viewarmy.icn'),
            children,
            border_width=37,    # TODO: may need separate w/h here
            state=State(monster_id=monster.id),
        )

    @staticmethod
    def icn_name(monster_icn_name):
        if monster_icn_name in WIP_ICN_MONSTERS:
            return f'{monster_icn_name}.wip'

        else:
            return f'{monster_icn_name}.wlk'

    def on_key_up(self, key):
        if key == pygame.K_ESCAPE:
            return fhomm.command.CMD_CLOSE
