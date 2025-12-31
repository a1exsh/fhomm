import pygame

import fhomm.ui
import fhomm.handler
from fhomm.render import Pos
import fhomm.window.new_battle


class Handler(fhomm.ui.Window):
    def __init__(self, loader):
        super().__init__()
        self.loader = loader
        self.bg_image = loader.load_image('redback.bmp')
        self.measure(self.bg_image.dim)

        buttons = [
            (0, pygame.K_s, self.cmd_standard_game),
            (2, pygame.K_c, self.cmd_campaign_game),
            (4, pygame.K_m, self.cmd_multiplayer_game),
            (4, pygame.K_b, self.cmd_battle),
            (6, pygame.K_ESCAPE, self.cmd_cancel),
        ]
        for i, (base_idx, key, cmd) in enumerate(buttons):
            self.attach(
                fhomm.ui.IcnButton(loader, 'btnnewgm.icn', base_idx, cmd, key),
                Pos(8, 20 + 66*i),
            )

    def on_render(self, ctx):
        self.bg_image.render(ctx)

    def cmd_standard_game(self):
        # return fhomm.handler.cmd_show(
        #     fhomm.window.new_game.Handler(self.loader),
        #     Pos(311, 14),
        # )
        pass

    def cmd_campaign_game(self):
        # return fhomm.handler.cmd_show(
        #     fhomm.window.load_game.Handler(self.loader),
        #     Pos(311, 14),
        # )
        pass

    def cmd_multiplayer_game(self):
        # return fhomm.handler.cmd_show(
        #     fhomm.window.high_scores.Handler(self.loader),
        #     Pos(0, 0),
        # )
        pass

    def cmd_battle(self):
        return fhomm.handler.cmd_show(
            fhomm.window.new_battle.Handler(self.loader),
            Pos((640 - 448)//2, (480 - 448)//2),
        )

    def cmd_cancel(self):
        return fhomm.handler.CMD_CLOSE
