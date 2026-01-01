import pygame

from fhomm.render import Pos
import fhomm.handler
import fhomm.ui
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
            fhomm.window.select_hero.Handler(self.loader),
            Pos(0, 74),
        )

    def cmd_select_defender(self):
        return fhomm.handler.cmd_show(
            fhomm.window.select_hero.Handler(self.loader),
            Pos(320, 74),
        )

    def cmd_cancel(self):
        return fhomm.handler.CMD_CLOSE
