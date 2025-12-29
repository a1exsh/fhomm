import pygame

import fhomm.palette
import fhomm.ui
from fhomm.ui import Pos, Rect


class Handler(fhomm.ui.Handler):
    def __init__(self, screen, loader):
        super().__init__(screen, loader)

        self.bg_image = self.loader.load_image('redback.bmp')
        self.rect = Rect(
            self.screen.get_width() - (self.bg_image.get_width() + 46),
            35,
            self.bg_image.get_width(),
            self.bg_image.get_height(),
        )
        self.attach(
            fhomm.ui.IcnButton(
                self.screen,
                self.loader,
                Pos(self.rect.x + 33, self.rect.y + 45),
                'btnmain.icn',
                2,
                pygame.K_n,     # new game
            )
        )
        self.attach(
            fhomm.ui.IcnButton(
                self.screen,
                self.loader,
                Pos(self.rect.x + 33, self.rect.y + 45 + 66),
                'btnmain.icn',
                0,
                pygame.K_l,     # load game
            )
        )
        self.attach(
            fhomm.ui.IcnButton(
                self.screen,
                self.loader,
                Pos(self.rect.x + 33, self.rect.y + 45 + 66*2),
                'btnmain.icn',
                4,
                pygame.K_s,     # high score
            )
        )
        self.attach(
            fhomm.ui.IcnButton(
                self.screen,
                self.loader,
                Pos(self.rect.x + 33, self.rect.y + 45 + 66*3),
                'btnmain.icn',
                6,
                pygame.K_c,     # credits
            )
        )
        self.attach(
            fhomm.ui.IcnButton(
                self.screen,
                self.loader,
                Pos(self.rect.x + 33, self.rect.y + 45 + 66*4),
                'btnmain.icn',
                8,
                pygame.K_q,     # quit
            )
        )

    def on_first_render(self):
        shadow_pos = Pos(16, 16)
        bg_area = Rect(
            self.rect.x,
            self.rect.y,
            self.rect.w + shadow_pos.x,
            self.rect.h + shadow_pos.y,
        )
        self.capture_background(rect=bg_area)

        bg_copy = pygame.Surface((bg_area.w, bg_area.h), depth=8)
        # TODO: get the pre-made shadow-safe palette from the Palette object
        bg_copy.set_palette(fhomm.palette.make_safe_for_shadow(self.screen.get_palette()))
        bg_copy.blit(self.captured_bg, (0, 0))

        shadow = pygame.Surface((self.rect.w, self.rect.h))
        shadow.set_alpha(96)
        bg_copy.blit(shadow, shadow_pos)

        self.screen.blit(bg_copy, (self.rect.x, self.rect.y))

    def on_detach(self):
        self.restore_background()

    def capture_background(self, rect=None):
        # TODO: assert before first render?
        if rect is None:
            rect = self.rect

        self.captured_bg = pygame.Surface((rect.w, rect.h), depth=8)
        self.captured_bg.set_palette(self.screen.get_palette())
        self.captured_bg.blit(self.screen, (0, 0), area=rect)

    def restore_background(self, pos=None):
        if pos is None:
            pos = Pos(self.rect.x, self.rect.y)

        self.screen.blit(self.captured_bg, pos)

    def on_render(self):
        self.bg_image.render(self.screen, Pos(self.rect.x, self.rect.y))
