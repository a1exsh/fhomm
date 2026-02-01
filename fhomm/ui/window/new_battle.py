from collections import namedtuple

import pygame

from fhomm.game.heroes import HEROES
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
            'aarmy1',
            'aart1',
        ],
        submodule='window.new_battle',
    )
):
    @staticmethod
    def set_attacker(attacker):
        return lambda s: s._replace(attacker=attacker)

    @staticmethod
    def set_defender(defender):
        return lambda s: s._replace(defender=defender)


class NewBattleWindow(fhomm.ui.Window):
    def __init__(self, toolkit):
        self.toolkit = toolkit

        attacker = 0
        defender = 35

        self.icn_attacker = self.toolkit.icon(
            self.hero_portrait_icn_name(attacker),
            action=self.cmd_select_attacker,
            hotkey=pygame.K_a,
        )
        self.icn_defender = self.toolkit.icon(
            self.hero_portrait_icn_name(defender),
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

            fhomm.ui.Window.Slot(self.icn_attacker, Pos(28, 44), 'icn_attacker'),
            fhomm.ui.Window.Slot(self.icn_defender, Pos(319, 44), 'icn_defender'),

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
                    lambda s: f"{HEROES[s.attacker].kind.default_stats.attack}",
                    font=toolkit.get_small_font(),
                ),
                Pos(134, 50),
                '_self',
            ),

            fhomm.ui.Window.Slot(
                toolkit.dynamic_label(
                    Size(44, 10),
                    lambda s: f"{HEROES[s.attacker].kind.default_stats.defense}",
                    font=toolkit.get_small_font(),
                ),
                Pos(134, 70),
                '_self',
            ),

            fhomm.ui.Window.Slot(
                toolkit.dynamic_label(
                    Size(44, 10),
                    lambda s: f"{HEROES[s.attacker].kind.default_stats.power}",
                    font=toolkit.get_small_font(),
                ),
                Pos(134, 90),
                '_self',
            ),

            fhomm.ui.Window.Slot(
                toolkit.dynamic_label(
                    Size(44, 10),
                    lambda s: f"{HEROES[s.attacker].kind.default_stats.knowledge}",
                    font=toolkit.get_small_font(),
                ),
                Pos(134, 110),
                '_self',
            ),

            # defender stats
            fhomm.ui.Window.Slot(
                toolkit.dynamic_label(
                    Size(44, 10),
                    lambda s: f"{HEROES[s.defender].kind.default_stats.attack}",
                    font=toolkit.get_small_font(),
                ),
                Pos(270, 50),
                '_self',
            ),

            fhomm.ui.Window.Slot(
                toolkit.dynamic_label(
                    Size(44, 10),
                    lambda s: f"{HEROES[s.defender].kind.default_stats.defense}",
                    font=toolkit.get_small_font(),
                ),
                Pos(270, 70),
                '_self',
            ),

            fhomm.ui.Window.Slot(
                toolkit.dynamic_label(
                    Size(44, 10),
                    lambda s: f"{HEROES[s.defender].kind.default_stats.power}",
                    font=toolkit.get_small_font(),
                ),
                Pos(270, 90),
                '_self',
            ),

            fhomm.ui.Window.Slot(
                toolkit.dynamic_label(
                    Size(44, 10),
                    lambda s: f"{HEROES[s.defender].kind.default_stats.knowledge}",
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
                'icn_attacker_army_1',
            ),

            # artifact selectors
            fhomm.ui.Window.Slot(
                self.toolkit.icon('artfx.icn', 37, action=self.cmd_select_artifact),
                Pos(76, 194),
                'icn_attacker_artifact_1',
            ),

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
        ]

        super().__init__(
            toolkit.load_image('swapwin.bmp'),
            children,
            border_width=4,
            state=State(
                attacker=attacker,
                defender=defender,
                aarmy1=23,
                aart1=1,
            ),
        )

    @staticmethod
    def hero_portrait_icn_name(idx):
        return "port%04d.icn" % idx

    def hero_portrait_img(self, idx):
        return self.toolkit.load_sprite(self.hero_portrait_icn_name(idx))

    @staticmethod
    def versus_label_text(state):
        return f"{HEROES[state.attacker].name} vs. {HEROES[state.defender].name}"

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
            ArmySelectorWindow(self.toolkit, 'aarmy1'),
            Pos(0, 74),
            'select_army',
        )

    def cmd_select_artifact(self):
        return fhomm.command.cmd_show(
            ArtifactSelectorWindow(self.toolkit, 'aart1'),
            Pos(0, 74),
            'select_artifact',
        )

    def cmd_cancel(self):
        return fhomm.command.CMD_CLOSE

    def on_return(self, key, value):
        if key == 'attacker':
            return fhomm.command.cmd_update(State.set_attacker(value)), \
                fhomm.command.cmd_update_other(
                    'icn_attacker',
                    fhomm.ui.button.ActiveIcon.State.set_image(
                        self.hero_portrait_img(value)
                    ),
                )

        elif key == 'defender':
            return fhomm.command.cmd_update(State.set_defender(value)), \
                fhomm.command.cmd_update_other(
                    'icn_defender',
                    fhomm.ui.button.ActiveIcon.State.set_image(
                        self.hero_portrait_img(value)
                    ),
                )
