import pygame

import fhomm.palette
import fhomm.ui
from fhomm.ui import Pos, Rect


class Handler(fhomm.ui.ShadowCastingWindow):
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

    def on_render(self):
        self.bg_image.render(self.screen, Pos(self.rect.x, self.rect.y))
