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
        self.buttons = [
            fhomm.ui.Button(
                Pos(self.pos.x + 33, self.pos.y + 45),
                self.loader.load_sprite('btnmain.icn', 2),
                self.loader.load_sprite('btnmain.icn', 3),
                pygame.K_n
            ),
            fhomm.ui.Button(
                Pos(self.pos.x + 33, self.pos.y + 45 + 66),
                self.loader.load_sprite('btnmain.icn', 0),
                self.loader.load_sprite('btnmain.icn', 1),
                pygame.K_l
            ),
            fhomm.ui.Button(
                Pos(self.pos.x + 33, self.pos.y + 45 + 66*2),
                self.loader.load_sprite('btnmain.icn', 4),
                self.loader.load_sprite('btnmain.icn', 5),
                pygame.K_s
            ),
            fhomm.ui.Button(
                Pos(self.pos.x + 33, self.pos.y + 45 + 66*3),
                self.loader.load_sprite('btnmain.icn', 6),
                self.loader.load_sprite('btnmain.icn', 7),
                pygame.K_c
            ),
            fhomm.ui.Button(
                Pos(self.pos.x + 33, self.pos.y + 45 + 66*4),
                self.loader.load_sprite('btnmain.icn', 8),
                self.loader.load_sprite('btnmain.icn', 9),
                pygame.K_q
            ),
        ]

    def on_event(self, event):
        if event.type == pygame.QUIT:
            return fhomm.handler.CMD_QUIT

        elif event.type == fhomm.handler.EVENT_INIT:
            return fhomm.handler.CMD_RENDER

        elif event.type == pygame.KEYDOWN:
            for button in self.buttons:
                if event.key == button.hotkey:
                    return fhomm.handler.CMD_QUIT

        elif event.type == pygame.MOUSEMOTION:
            #print(event)
            changed = False
            mouse_pos = Pos(event.pos[0], event.pos[1])
            for button in self.buttons:
                if fhomm.ui.pos_in_rect(mouse_pos, button.rect):
                    changed = changed or button.set_pressed()
                else:
                    changed = changed or button.set_released()
            if changed:
                return fhomm.handler.CMD_RENDER

    def render(self):
        self.bg_image.render(self.screen, self.pos)
        for button in self.buttons:
            button.render(self.screen)
