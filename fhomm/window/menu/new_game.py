import pygame

from fhomm.render import Pos
from fhomm.window.new_battle import NewBattleWindow
import fhomm.handler
import fhomm.ui


class NewGameMenu(fhomm.ui.Window):
    def __init__(self, toolkit):
        super().__init__(toolkit.load_image('redback.bmp'), border_width=25)
        self.toolkit = toolkit

        buttons = [
            (0, pygame.K_s, self.cmd_standard_game),
            (2, pygame.K_c, self.cmd_campaign_game),
            (4, pygame.K_m, self.cmd_multiplayer_game),
            (4, pygame.K_b, self.cmd_battle),
            (6, pygame.K_ESCAPE, self.cmd_cancel),
        ]
        for i, (base_idx, key, cmd) in enumerate(buttons):
            self.attach(
                toolkit.button('btnnewgm.icn', base_idx, action=cmd, hotkey=key),
                Pos(33, 45 + 66*i),
            )

    def on_render(self, ctx):
        self.bg_image.render(ctx)

    def cmd_standard_game(self):
        # return fhomm.handler.cmd_show(
        #     fhomm.window.new_game.Handler(self.toolkit),
        #     Pos(311, 14),
        # )
        pass

    def cmd_campaign_game(self):
        # return fhomm.handler.cmd_show(
        #     fhomm.window.load_game.Handler(self.toolkit),
        #     Pos(311, 14),
        # )
        pass

    def cmd_multiplayer_game(self):
        # return fhomm.handler.cmd_show(
        #     fhomm.window.high_scores.Handler(self.toolkit),
        #     Pos(0, 0),
        # )
        pass

    def cmd_battle(self):
        return fhomm.handler.cmd_show(
            NewBattleWindow(self.toolkit),
            Pos((640 - 448)//2, (480 - 448)//2), # TODO: ask WindowManager to center
        )

    def cmd_cancel(self):
        return fhomm.handler.CMD_CLOSE
