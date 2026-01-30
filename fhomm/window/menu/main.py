import pygame

from fhomm.window.credits import CreditsScreen
from fhomm.window.high_scores import HighScoresWindow
from fhomm.window.menu.new_game import NewGameMenu
from fhomm.window.menu.load_game import LoadGameMenu
from fhomm.render import Pos
import fhomm.command
import fhomm.ui


class MainMenu(fhomm.ui.Window):
    def __init__(self, toolkit):
        self.toolkit = toolkit

        buttons = [
            (2, pygame.K_n, self.cmd_new_game, 'new_game'),
            (0, pygame.K_l, self.cmd_load_game, 'load_game'),
            (4, pygame.K_h, self.cmd_high_scores, 'high_scores'),
            (6, pygame.K_c, self.cmd_credits, 'credits'),
            (8, pygame.K_q, self.cmd_quit, 'quit'),
        ]
        children = [
            fhomm.ui.Window.Slot(
                toolkit.button('btnmain.icn', base_idx, action=cmd, hotkey=key),
                Pos(33, 45 + 66*i),
                key=f"btn_{name}",
            )
            for i, (base_idx, key, cmd, name) in enumerate(buttons)
        ]

        super().__init__(
            toolkit.load_image('redback.bmp'),
            children,
            border_width=25,
        )

    def on_render(self, ctx, _):
        self.bg_image.render(ctx)

    def on_key_up(self, key):
        if key == pygame.K_ESCAPE:
            return fhomm.command.CMD_QUIT

    def cmd_new_game(self):
        return fhomm.command.cmd_show(
            NewGameMenu(self.toolkit), Pos(401, 35), 'new_game'
        )

    def cmd_load_game(self):
        return fhomm.command.cmd_show(
            LoadGameMenu(self.toolkit), Pos(311, 14), 'load_game'
        )

    def cmd_high_scores(self):
        return fhomm.command.cmd_show(
            HighScoresWindow(self.toolkit), Pos(0, 0), 'high_scores'
        )

    def cmd_credits(self):
        return fhomm.command.cmd_show(
            CreditsScreen(self.toolkit), Pos(0, 0), 'credits'
        )

    def cmd_quit(self):
        return fhomm.command.CMD_QUIT

    def on_quit(self):
        return fhomm.command.CMD_QUIT
