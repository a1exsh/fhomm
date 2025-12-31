import pygame

import fhomm.ui
import fhomm.handler
import fhomm.window.new_game
import fhomm.window.credits
from fhomm.render import Pos


class Handler(fhomm.ui.Window):
    def __init__(self, loader):
        super().__init__()
        self.bg_image = loader.load_image('redback.bmp')
        self.measure(self.bg_image.dim)

        cmd_new = lambda: fhomm.handler.cmd_show(
            fhomm.window.new_game.Handler(loader),
            Pos(311, 14),
        )
        cmd_load = lambda: fhomm.handler.cmd_show(
            fhomm.window.credits.Handler(loader),
            Pos(0, 0),
        )
        cmd_scores = lambda: fhomm.handler.cmd_show(
            fhomm.window.credits.Handler(loader),
            Pos(0, 0),
        )
        cmd_credits = lambda: fhomm.handler.cmd_show(
            fhomm.window.credits.Handler(loader),
            Pos(0, 0),
        )
        cmd_quit = lambda: fhomm.handler.CMD_QUIT
        buttons = [
            (2, pygame.K_n, cmd_new),
            (0, pygame.K_l, cmd_load),
            (4, pygame.K_s, cmd_scores),
            (6, pygame.K_c, cmd_credits),
            (8, pygame.K_q, cmd_quit),
        ]
        for i, (base_idx, key, cmd) in enumerate(buttons):
            self.attach(
                fhomm.ui.IcnButton(loader, 'btnmain.icn', base_idx, cmd, key),
                Pos(8, 20 + 66*i),
            )

    def on_render(self, ctx):
        self.bg_image.render(ctx)
