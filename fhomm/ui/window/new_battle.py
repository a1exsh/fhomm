from collections import namedtuple

import pygame

from fhomm.game.artifacts import ARTIFACTS
from fhomm.game.heroes import HEROES, Hero
from fhomm.render import Pos, Size, Rect
from fhomm.ui.window.select.army import ArmySelectorWindow
from fhomm.ui.window.select.artifact import ArtifactSelectorWindow
from fhomm.ui.window.select.hero import HeroSelectorWindow
import fhomm.command
import fhomm.render
import fhomm.toolkit
import fhomm.ui
import fhomm.ui.button


class SmallArmyIcon(fhomm.ui.button.ActiveArea):
    def __init__(self, toolkit, monster=None, count=None, **kwargs):
        super().__init__(Size(34, 44), SmallArmyIcon.State(), **kwargs)
        self.toolkit = toolkit
        self.monster = monster
        self.count = count

        self._bg_capture = None

    def on_render(self, ctx, _):
        if self._bg_capture is None:
            self._bg_capture = ctx.capture(self.rect)
        else:
            self._bg_capture.render(ctx)

        if self.monster is not None:
            img = self.toolkit.load_sprite('mons32.icn', self.monster)
            img.render(ctx, Pos(1, 1))

        if self.count is not None:
            self.toolkit.get_small_font().draw_text(
                ctx,
                str(self.count),
                Rect.ltrb(0, 37, self.size.w, self.size.h),
                halign=fhomm.render.CENTER,
            )


class State(
    fhomm.ui.state_tuple(
        [
            'attacker',
            'defender',
            'aarmy0',
        ],
        submodule='window.new_battle',
    )
):
    @staticmethod
    def set_attacker(attacker):
        return lambda s: s._replace(attacker=attacker)

    @staticmethod
    def update_attacker(update_fn):
        return lambda s: s._replace(attacker=update_fn(s.attacker))

    @staticmethod
    def set_defender(defender):
        return lambda s: s._replace(defender=defender)


class NewBattleWindow(fhomm.ui.Window):
    def __init__(self, toolkit):
        self.toolkit = toolkit

        attacker_idx = 0
        defender_idx = len(HEROES) - 1
        attacker = HEROES[attacker_idx]
        defender = HEROES[defender_idx]

        self.icn_attacker = self.toolkit.dynamic_icon(
            Size(101, 93),
            lambda _, win: self.hero_portrait_img(win.attacker.id),
            action=self.cmd_select_attacker,
            hotkey=pygame.K_a,
        )
        self.icn_defender = self.toolkit.dynamic_icon(
            Size(101, 93),
            lambda _, win: self.hero_portrait_img(win.defender.id),
            action=self.cmd_select_defender,
            hotkey=pygame.K_d,
        )

        children = [
            fhomm.ui.Window.Slot(
                toolkit.dynamic_label(
                    Size(337, 22),
                    NewBattleWindow.versus_label_text,
                ),
                Pos(56, 9),
                '_self',
            ),

            fhomm.ui.Window.Slot(
                self.icn_attacker, Pos(28, 44), 'icn_attacker', '_self'
            ),
            fhomm.ui.Window.Slot(
                self.icn_defender, Pos(319, 44), 'icn_defender', '_self'
            ),

            # heroes stats labels
            fhomm.ui.Window.Slot(
                toolkit.label(
                    Size(92, 10),
                    "Attack Skill",
                    font=toolkit.get_small_font(),
                ),
                Pos(178, 50),
                'lbl_attack_skill',
            ),

            fhomm.ui.Window.Slot(
                toolkit.label(
                    Size(92, 10),
                    "Defense Skill",
                    font=toolkit.get_small_font(),
                ),
                Pos(178, 70),
                'lbl_defense_skill',
            ),

            fhomm.ui.Window.Slot(
                toolkit.label(
                    Size(92, 10),
                    "Spell Power",
                    font=toolkit.get_small_font(),
                ),
                Pos(178, 90),
                'lbl_spell_power',
            ),

            fhomm.ui.Window.Slot(
                toolkit.label(
                    Size(92, 10),
                    "Knowledge",
                    font=toolkit.get_small_font(),
                ),
                Pos(178, 110),
                'lbl_knowledge',
            ),

            # attacker stats
            fhomm.ui.Window.Slot(
                toolkit.dynamic_label(
                    Size(44, 10),
                    lambda s: f"{s.attacker.stats.attack}",
                    font=toolkit.get_small_font(),
                ),
                Pos(134, 50),
                '_self',
            ),

            fhomm.ui.Window.Slot(
                toolkit.dynamic_label(
                    Size(44, 10),
                    lambda s: f"{s.attacker.stats.defense}",
                    font=toolkit.get_small_font(),
                ),
                Pos(134, 70),
                '_self',
            ),

            fhomm.ui.Window.Slot(
                toolkit.dynamic_label(
                    Size(44, 10),
                    lambda s: f"{s.attacker.stats.power}",
                    font=toolkit.get_small_font(),
                ),
                Pos(134, 90),
                '_self',
            ),

            fhomm.ui.Window.Slot(
                toolkit.dynamic_label(
                    Size(44, 10),
                    lambda s: f"{s.attacker.stats.knowledge}",
                    font=toolkit.get_small_font(),
                ),
                Pos(134, 110),
                '_self',
            ),

            # defender stats
            fhomm.ui.Window.Slot(
                toolkit.dynamic_label(
                    Size(44, 10),
                    lambda s: f"{s.defender.stats.attack}",
                    font=toolkit.get_small_font(),
                ),
                Pos(270, 50),
                '_self',
            ),

            fhomm.ui.Window.Slot(
                toolkit.dynamic_label(
                    Size(44, 10),
                    lambda s: f"{s.defender.stats.defense}",
                    font=toolkit.get_small_font(),
                ),
                Pos(270, 70),
                '_self',
            ),

            fhomm.ui.Window.Slot(
                toolkit.dynamic_label(
                    Size(44, 10),
                    lambda s: f"{s.defender.stats.power}",
                    font=toolkit.get_small_font(),
                ),
                Pos(270, 90),
                '_self',
            ),

            fhomm.ui.Window.Slot(
                toolkit.dynamic_label(
                    Size(44, 10),
                    lambda s: f"{s.defender.stats.knowledge}",
                    font=toolkit.get_small_font(),
                ),
                Pos(270, 110),
                '_self',
            ),

            # army selectors
            fhomm.ui.Window.Slot(
                SmallArmyIcon(
                    self.toolkit,
                    monster=23,
                    count=1,
                    action=self.cmd_select_army,
                ),
                Pos(23, 147),
                'icn_attacker_army_0',
            ),
        ]

        # artifact selectors
        children.extend(
            self.artifact_slot('attacker', Pos(76, 194), x, y)
            for x in range(2)
            for y in range(7)
        )

        children.append(
            # EXIT
            fhomm.ui.Window.Slot(
                self.toolkit.button(
                    'swapbtn.icn',
                    0,
                    action=self.cmd_cancel,
                    hotkey=pygame.K_ESCAPE,
                ),
                Pos(184, 413),
                'btn_exit',
            ),
        )

        super().__init__(
            toolkit.load_image('swapwin.bmp'),
            children,
            border_width=4,
            state=State(
                attacker=attacker,
                defender=defender,
                aarmy0=23,
            ),
        )

    @staticmethod
    def hero_portrait_icn_name(idx):
        return "port%04d.icn" % idx

    def hero_portrait_img(self, idx):
        return self.toolkit.load_sprite(self.hero_portrait_icn_name(idx))

    def artifact_slot(self, hero_role, top_left, x, y):
        def slot_artifact_img(_, win):
            artifact = getattr(win, hero_role).artifacts[7*x + y]
            return self.artifact_img(artifact.id) if artifact else None

        idx = 7*x + y
        return fhomm.ui.Window.Slot(
            self.toolkit.dynamic_icon(
                Size(32, 32),
                slot_artifact_img,
                action=self.cmd_select_artifact(f'{hero_role}_artifact_{idx}'),
            ),
            Pos(35*x, 35*y).moved_by(top_left),
            f'icn_{hero_role}_artifact_{idx}',
            '_self',
        )

    def artifact_img(self, idx):
        return self.toolkit.load_sprite('artfx.icn', idx)

    @staticmethod
    def versus_label_text(state):
        return f"{state.attacker.name} vs. {state.defender.name}"

    def cmd_select_attacker(self):
        return fhomm.command.cmd_show(
            HeroSelectorWindow(
                self.toolkit,
                "Select Attacking Hero:",
                'attacker',
            ),
            Pos(0, 74),
            'select_hero',
        )

    def cmd_select_defender(self):
        return fhomm.command.cmd_show(
            HeroSelectorWindow(
                self.toolkit,
                "Select Defending Hero:",
                'defender',
            ),
            Pos(320, 74),
            'select_hero',
        )

    def cmd_select_army(self):
        return fhomm.command.cmd_show(
            ArmySelectorWindow(self.toolkit, 'aarmy0'),
            Pos(0, 74),
            'select_army',
        )

    def cmd_select_artifact(self, key):
        def cmd():
            return fhomm.command.cmd_show(
                ArtifactSelectorWindow(self.toolkit, key),
                Pos(0, 74),
                'select_artifact',
            )

        return cmd

    def cmd_cancel(self):
        return fhomm.command.CMD_CLOSE

    def on_return(self, key, value):
        if key == 'attacker':
            return fhomm.command.cmd_update(State.set_attacker(HEROES[value]))

        elif key == 'defender':
            return fhomm.command.cmd_update(State.set_defender(HEROES[value]))

        elif key.startswith('attacker_artifact_'):
            idx = int(key[len('attacker_artifact_'):])

            return fhomm.command.cmd_update(
                State.update_attacker(Hero.set_artifact(idx, ARTIFACTS[value]))
            )
