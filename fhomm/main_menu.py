import pygame

import fhomm.handler
from fhomm.ui import Pos


class Handler(fhomm.handler.Handler):
    def __init__(self, screen, loader):
        super().__init__(screen, loader)

        self.bg_image = self.loader.load_image('redback.bmp')
        self.pos = Pos(
            self.screen.get_width() - (self.bg_image.get_width() + 46),
            35
        )
        self.children = [
            fhomm.ui.IcnButton(
                self.screen,
                self.loader,
                Pos(self.pos.x + 33, self.pos.y + 45),
                'btnmain.icn',
                2,
                pygame.K_n,
            ),
            fhomm.ui.IcnButton(
                self.screen,
                self.loader,
                Pos(self.pos.x + 33, self.pos.y + 45 + 66),
                'btnmain.icn',
                0,
                pygame.K_l,
            ),
            fhomm.ui.IcnButton(
                self.screen,
                self.loader,
                Pos(self.pos.x + 33, self.pos.y + 45 + 66*2),
                'btnmain.icn',
                4,
                pygame.K_s,
            ),
            fhomm.ui.IcnButton(
                self.screen,
                self.loader,
                Pos(self.pos.x + 33, self.pos.y + 45 + 66*3),
                'btnmain.icn',
                6,
                pygame.K_c,
            ),
            fhomm.ui.IcnButton(
                self.screen,
                self.loader,
                Pos(self.pos.x + 33, self.pos.y + 45 + 66*4),
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
        shadow = pygame.Surface((self.bg_image.get_width(), self.bg_image.get_height()))
        shadow.set_alpha(96)

        # overwrite the cycling blocks in the palette to avoid mapping to them due to blend
        org = list(self.screen.get_palette()) # it's a tuple, so make a copy to assign
        pal = list(org)
        pal[224:232] = [(255, 255, 255)]*8
        pal[240:251] = [(255, 255, 255)]*11
        self.screen.set_palette(pal)
        self.screen.blit(shadow, (self.pos.x + 16, self.pos.y + 16))
        self.screen.set_palette(org)

        self.bg_image.render(self.screen, self.pos)
