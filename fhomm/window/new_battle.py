from collections import namedtuple

import pygame

from fhomm.game.heroes import HEROES
from fhomm.render import Pos, Size, Rect
from fhomm.window.select.army import ArmySelectorWindow
from fhomm.window.select.artifact import ArtifactSelectorWindow
from fhomm.window.select.hero import HeroSelectorWindow
import fhomm.handler
import fhomm.render
import fhomm.toolkit
import fhomm.ui
import fhomm.ui.button


class SmallArmyIcon(fhomm.ui.button.ActiveArea):
    def __init__(self, toolkit, monster=None, count=None, **kwargs):
        super().__init__(Size(34, 44), **kwargs)
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
    namedtuple(
        'State',
        [
            'attacker',
            'defender',
            'aarmy1',
            'aart1',
        ],
        module='fhomm.window.new_battle',
    )
):
    __slots__ = ()

    @staticmethod
    def set_attacker(attacker):
        return lambda s: s._replace(attacker=attacker)

    @staticmethod
    def set_defender(defender):
        return lambda s: s._replace(defender=defender)


class NewBattleWindow(fhomm.ui.Window):
    def __init__(self, toolkit):
        self.toolkit = toolkit

        self.icn_attacker = self.toolkit.icon(
            'port0000.icn',
            action=self.cmd_select_attacker,
            hotkey=pygame.K_a,
        )
        self.icn_defender = self.toolkit.icon(
            'port0035.icn',
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
                attacker=0,
                defender=35,
                aarmy1=23,
                aart1=1,
            ),
        )

    @staticmethod
    def versus_label_text(state):
        return f"{HEROES[state.attacker].name} vs. {HEROES[state.defender].name}"

    def cmd_select_attacker(self):
        return fhomm.handler.cmd_show(
            HeroSelectorWindow(
                self.toolkit,
                "Select Attacking Hero:",
                'attacker',
            ),
            Pos(0, 74),
            'select_hero',
        )

    def cmd_select_defender(self):
        return fhomm.handler.cmd_show(
            HeroSelectorWindow(
                self.toolkit,
                "Select Defending Hero:",
                'defender',
            ),
            Pos(320, 74),
            'select_hero',
        )

    def cmd_select_army(self):
        return fhomm.handler.cmd_show(
            ArmySelectorWindow(self.toolkit, 'aarmy1'),
            Pos(0, 74),
            'select_army',
        )

    def cmd_select_artifact(self):
        return fhomm.handler.cmd_show(
            ArtifactSelectorWindow(self.toolkit, 'aart1'),
            Pos(0, 74),
            'select_artifact',
        )

    def cmd_cancel(self):
        return fhomm.handler.CMD_CLOSE

    # TODO: rename to on_return
    def on_window_closed(self, key, value):
        if key == 'attacker':
            self.icn_attacker.set_image(
                self.toolkit.load_sprite("port%04d.icn" % value)
            )
            return fhomm.handler.cmd_update(State.set_attacker(value))

        elif key == 'defender':
            self.icn_defender.set_image(
                self.toolkit.load_sprite("port%04d.icn" % value)
            )
            return fhomm.handler.cmd_update(State.set_defender(value))
