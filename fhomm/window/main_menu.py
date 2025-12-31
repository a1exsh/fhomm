import pygame

import fhomm.ui
import fhomm.handler
import fhomm.window.new_game
import fhomm.window.credits
import fhomm.window.high_scores
from fhomm.render import Pos


class Handler(fhomm.ui.Window):
    def __init__(self, loader):
        super().__init__()
        self.loader = loader
        self.bg_image = loader.load_image('redback.bmp')
        self.measure(self.bg_image.dim)

        buttons = [
            (2, pygame.K_n, self.cmd_new_game),
            (0, pygame.K_l, self.cmd_load_game),
            (4, pygame.K_h, self.cmd_high_scores),
            (6, pygame.K_c, self.cmd_credits),
            (8, pygame.K_q, self.cmd_quit),
        ]
        for i, (base_idx, key, cmd) in enumerate(buttons):
            self.attach(
                fhomm.ui.IcnButton(loader, 'btnmain.icn', base_idx, cmd, key),
                Pos(8, 20 + 66*i),
            )

    def on_render(self, ctx):
        self.bg_image.render(ctx)

    def cmd_new_game(self):
        return fhomm.handler.cmd_show(
            fhomm.window.new_game.Handler(self.loader),
            Pos(311, 14),
        )

    def cmd_load_game(self):
        return fhomm.handler.cmd_show(
            fhomm.window.credits.Handler(self.loader),
            Pos(0, 0),
        )

    def cmd_high_scores(self):
        return fhomm.handler.cmd_show(
            fhomm.window.high_scores.Handler(self.loader),
            Pos(0, 0),
        )

    def cmd_credits(self):
        return fhomm.handler.cmd_show(
            fhomm.window.credits.Handler(self.loader),
            Pos(0, 0),
        )

    def cmd_quit(self):
        return fhomm.handler.CMD_QUIT
