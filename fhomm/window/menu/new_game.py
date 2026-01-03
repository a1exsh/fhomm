import pygame

from fhomm.render import Pos, Rect
from fhomm.window.new_battle import NewBattleWindow
import fhomm.handler
import fhomm.render
import fhomm.ui
import fhomm.ui.element


class NewGameMenu(fhomm.ui.Window):
    def __init__(self, toolkit):
        super().__init__(toolkit.load_image('redback.bmp'), border_width=25)
        self.toolkit = toolkit

        buttons = [
            (0, 0, pygame.K_s, self.cmd_standard_game),
            (1, 2, pygame.K_c, self.cmd_campaign_game),
            (2, 4, pygame.K_m, self.cmd_multiplayer_game),
            # (3, 4, pygame.K_b, self.cmd_battle),
            (4, 6, pygame.K_ESCAPE, self.cmd_cancel),
        ]
        for i, base_idx, key, cmd in buttons:
            self.attach(
                toolkit.button('btnnewgm.icn', base_idx, action=cmd, hotkey=key),
                Pos(33, 45 + 66*i),
            )

        self.attach(
            fhomm.ui.element.ActiveIcon(
                NewGameMenu.get_battle_button(toolkit),
                action=self.cmd_battle,
                hotkey=pygame.K_b,
            ),
            Pos(33, 45 + 66*3),
        )

    @classmethod
    def get_battle_button(cls, toolkit):
        img = toolkit.load_sprite('btnnewgm.icn', 6).make_copy()
        ctx = img.get_context()
        ctx.draw_rect(126, Rect.ltrb(25, 21, 104, 34)) # clear
        toolkit.get_button_font().draw_multiline_text(
            ctx,
            "BATTLE ONLY",
            Rect.ltrb(12, 12, 114, 43),
        )
        return img

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
