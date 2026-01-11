import pygame

from fhomm.render import Pos, Size, Rect
from fhomm.window.select.army import ArmySelectorWindow
from fhomm.window.select.artifact import ArtifactSelectorWindow
from fhomm.window.select.hero import HeroSelectorWindow
import fhomm.handler
import fhomm.render
import fhomm.toolkit
import fhomm.ui
import fhomm.ui.element


class SmallArmyIcon(fhomm.ui.element.ActiveArea):
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
        super().__init__(toolkit.load_image('swapwin.bmp'), border_width=4)
        self.toolkit = toolkit

        self.attach(
            self.toolkit.icon(
                'port0000.icn',
                0,
                action=self.cmd_select_attacker,
                hotkey=pygame.K_a, # attacker
            ),
            Pos(28, 44),
        )

        self.attach(
            self.toolkit.icon(
                'port0035.icn',
                0,
                action=self.cmd_select_defender,
                hotkey=pygame.K_d, # defender
            ),
            Pos(319, 44),
        )

        # army selectors
        self.attach(
            SmallArmyIcon(
                self.toolkit,
                monster=23,
                count=1,
                action=self.cmd_select_army,
            ),
            Pos(23, 147),
        )

        # artifact selectors
        self.attach(
            self.toolkit.icon('artfx.icn', 37, action=self.cmd_select_artifact),
            Pos(76, 194),
        )

        # EXIT
        self.attach(
            self.toolkit.button(
                'swapbtn.icn',
                0,
                action=self.cmd_cancel,
                hotkey=pygame.K_ESCAPE,
            ),
            Pos(184, 413),
        )

    def cmd_select_attacker(self):
        return fhomm.handler.cmd_show(
            HeroSelectorWindow(self.toolkit, "Select Attacking Hero:"),
            Pos(0, 74),
        )

    def cmd_select_defender(self):
        return fhomm.handler.cmd_show(
            HeroSelectorWindow(self.toolkit, "Select Defending Hero:"),
            Pos(320, 74),
        )

    def cmd_select_army(self):
        return fhomm.handler.cmd_show(
            ArmySelectorWindow(self.toolkit),
            Pos(0, 74),
        )

    def cmd_select_artifact(self):
        return fhomm.handler.cmd_show(
            ArtifactSelectorWindow(self.toolkit),
            Pos(0, 74),
        )

    def cmd_cancel(self):
        return fhomm.handler.CMD_CLOSE
