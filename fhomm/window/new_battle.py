import pygame

from fhomm.render import Pos
import fhomm.handler
import fhomm.ui
import fhomm.window.select_army
import fhomm.window.select_artifact
import fhomm.window.select_hero


class Handler(fhomm.ui.Window):
    def __init__(self, loader):
        super().__init__(border_width=4)
        self.loader = loader
        self.bg_image = loader.load_image('swapwin.bmp')
        self.measure(self.bg_image.dim)

        self.attach(
            fhomm.ui.ImgButton(
                self.loader.load_sprite('port0000.icn', 0),
                self.cmd_select_attacker,
                hotkey=pygame.K_a, # attacker
            ),
            Pos(24, 40),
        )

        self.attach(
            fhomm.ui.ImgButton(
                self.loader.load_sprite('port0035.icn', 0),
                self.cmd_select_defender,
                hotkey=pygame.K_d, # defender
            ),
            Pos(315, 40),
        )

        self.attach(
            fhomm.ui.ImgButton(
                self.loader.load_sprite('mons32.icn', 23),
                self.cmd_select_army,
            ),
            Pos(20, 144),
        )

        self.attach(
            fhomm.ui.ImgButton(
                self.loader.load_sprite('artfx.icn', 37),
                self.cmd_select_artifact,
            ),
            Pos(72, 190),
        )

        # EXIT
        self.attach(
            fhomm.ui.IcnButton(
                self.loader,
                'swapbtn.icn',
                0,
                self.cmd_cancel,
                pygame.K_ESCAPE,
            ),
            Pos(180, 409),
        )

    def on_render(self, ctx):
        self.bg_image.render(ctx)

    def cmd_select_attacker(self):
        return fhomm.handler.cmd_show(
            fhomm.window.select_hero.Handler(
                self.loader,
                "Select Attacking Hero",
            ),
            Pos(0, 74),
        )

    def cmd_select_defender(self):
        return fhomm.handler.cmd_show(
            fhomm.window.select_hero.Handler(
                self.loader,
                "Select Defending Hero",
            ),
            Pos(320, 74),
        )

    def cmd_select_army(self):
        return fhomm.handler.cmd_show(
            fhomm.window.select_army.Handler(self.loader),
            Pos(0, 74),
        )

    def cmd_select_artifact(self):
        return fhomm.handler.cmd_show(
            fhomm.window.select_artifact.Handler(self.loader),
            Pos(0, 74),
        )

    def cmd_cancel(self):
        return fhomm.handler.CMD_CLOSE
