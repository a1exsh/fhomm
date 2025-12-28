import pygame

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
        self.children = [
            fhomm.ui.IcnButton(
                self.screen,
                self.loader,
                Pos(self.rect.x + 33, self.rect.y + 45),
                'btnmain.icn',
                2,
                pygame.K_n,
            ),
            fhomm.ui.IcnButton(
                self.screen,
                self.loader,
                Pos(self.rect.x + 33, self.rect.y + 45 + 66),
                'btnmain.icn',
                0,
                pygame.K_l,
            ),
            fhomm.ui.IcnButton(
                self.screen,
                self.loader,
                Pos(self.rect.x + 33, self.rect.y + 45 + 66*2),
                'btnmain.icn',
                4,
                pygame.K_s,
            ),
            fhomm.ui.IcnButton(
                self.screen,
                self.loader,
                Pos(self.rect.x + 33, self.rect.y + 45 + 66*3),
                'btnmain.icn',
                6,
                pygame.K_c,
            ),
            fhomm.ui.IcnButton(
                self.screen,
                self.loader,
                Pos(self.rect.x + 33, self.rect.y + 45 + 66*4),
                'btnmain.icn',
                8,
                pygame.K_q,
            ),
        ]

    # def on_event(self, event):

        # elif event.type == pygame.KEYDOWN:
        #     for button in self.buttons:
        #         if event.key == button.hotkey:
        #             return fhomm.handler.CMD_QUIT

        # if event.type == pygame.MOUSEMOTION:
        #     #print(event)
        #     changed = False
        #     mouse_pos = Pos(event.pos[0], event.pos[1])
        #     for button in self.buttons:
        #         if fhomm.ui.pos_in_rect(mouse_pos, button.rect):
        #             changed = changed or button.set_pressed()
        #         else:
        #             changed = changed or button.set_released()
        #     if changed:
        #         return fhomm.handler.CMD_RENDER

    def on_render(self):
        # overwrite the cycling blocks in the palette to avoid mapping to them due to blend
        org = list(self.screen.get_palette()) # it's a tuple, so make a copy to assign
        pal = list(org)
        pal[224:232] = [(255, 255, 255)]*8
        pal[240:251] = [(255, 255, 255)]*11

        # capture background in on_attach: restore in on_detach
        background = pygame.Surface((self.bg_image.get_width(), self.bg_image.get_height()), depth=8)
        background.set_palette(pal)
        background.blit(
            self.screen,
            (0, 0),
            area=(self.rect.x + 16, self.rect.y + 16, background.get_width(), background.get_height()),
        )

        shadow = pygame.Surface((self.bg_image.get_width(), self.bg_image.get_height()))
        shadow.set_alpha(96)
        background.blit(shadow, (0, 0))

        self.screen.blit(background, (self.rect.x + 16, self.rect.y + 16))

        self.bg_image.render(self.screen, Pos(self.rect.x, self.rect.y))
