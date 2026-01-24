import pygame

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


class NewBattleWindow(fhomm.ui.Window):
    def __init__(self, toolkit):
        self.toolkit = toolkit

        children = [
            fhomm.ui.Window.Slot(
                self.toolkit.icon(
                    'port0000.icn',
                    0,
                    action=self.cmd_select_attacker,
                    hotkey=pygame.K_a,
                ),
                Pos(28, 44),
                'icn_attacker',
            ),

            fhomm.ui.Window.Slot(
                self.toolkit.icon(
                    'port0035.icn',
                    0,
                    action=self.cmd_select_defender,
                    hotkey=pygame.K_d,
                ),
                Pos(319, 44),
                'icn_defender',
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
        )

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
            HeroSelectorWindow(self.toolkit, "Select Defending Hero:"),
            Pos(320, 74),
            'select_hero',
        )

    def cmd_select_army(self):
        return fhomm.handler.cmd_show(
            ArmySelectorWindow(self.toolkit),
            Pos(0, 74),
            'select_army',
        )

    def cmd_select_artifact(self):
        return fhomm.handler.cmd_show(
            ArtifactSelectorWindow(self.toolkit),
            Pos(0, 74),
            'select_artifact',
        )

    def cmd_cancel(self):
        return fhomm.handler.CMD_CLOSE

    def on_window_closed(self, key, value):
        if key == 'attacker':
            print(f"attacker => {value}")
