import pygame

import fhomm.handler


class Handler(fhomm.handler.Handler):
    def run(self):
        if self.first_run:
            self.first_run = False
            self.render()
            return fhomm.handler.RENDER

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return fhomm.handler.QUIT
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return fhomm.handler.QUIT

    def render(self):
        REDBACK = self.loader.load_bmp('redback.bmp')
        BTNNEW = self.loader.load_sprite('btnmain.icn', 2)
        # BTNLOAD = sprite_to_sdl(BTNMAIN[0])
        # BTNSCORE = sprite_to_sdl(BTNMAIN[4])
        # BTNCREDITS = sprite_to_sdl(BTNMAIN[6])
        # BTNQUIT = sprite_to_sdl(BTNMAIN[8])

        menu_pos = (self.screen.get_width() - (REDBACK.get_width() + 46), 35)
        self.screen.blit(REDBACK, menu_pos)
        self.screen.blit(BTNNEW,     (menu_pos[0] + 33, menu_pos[1] + 45))
        # self.screen.blit(BTNLOAD,    (menu_pos[0] + 33, menu_pos[1] + 45 + 66))
        # self.screen.blit(BTNSCORE,   (menu_pos[0] + 33, menu_pos[1] + 45 + 66*2))
        # self.screen.blit(BTNCREDITS, (menu_pos[0] + 33, menu_pos[1] + 45 + 66*3))
        # self.screen.blit(BTNQUIT,    (menu_pos[0] + 33, menu_pos[1] + 45 + 66*4))
