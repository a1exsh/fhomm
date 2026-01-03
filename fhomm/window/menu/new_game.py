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
            fhomm.ui.element.Button(
                NewGameMenu.get_battle_button(toolkit, is_pressed=False),
                NewGameMenu.get_battle_button(toolkit, is_pressed=True),
                action=self.cmd_battle,
                hotkey=pygame.K_b,
            ),
            Pos(33, 45 + 66*3),
        )

    @classmethod
    def get_battle_button(cls, toolkit, is_pressed):
        icn_idx = 6
        color_bg = 126
        clear_rect = Rect.ltrb(25, 21, 104, 34)
        text_rect = Rect.ltrb(12, 12, 114, 43)
        font = toolkit.get_button_font()

        if is_pressed:
            icn_idx += 1
            color_bg = 128
            clear_rect = clear_rect.offset(Pos(-2, 2))
            text_rect = text_rect.offset(Pos(-2, 2))
            font = toolkit.get_pressed_button_font()

        # CANCEL
        img = toolkit.load_sprite('btnnewgm.icn', icn_idx).make_copy()
        ctx = img.get_context()
        ctx.draw_rect(color_bg, clear_rect)
        font.draw_multiline_text(ctx, "BATTLE ONLY", text_rect,)

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
