import pygame

import fhomm.palette
import fhomm.ui
from fhomm.render import Pos, Dim, Rect


class Handler(fhomm.ui.Window): #ShadowCastingWindow
    def __init__(self, loader):
        super().__init__()
        self.bg_image = loader.load_image('redback.bmp')
        self.measure(self.bg_image.dim)

        buttons = [
            (2, pygame.K_n),    # new game
            (0, pygame.K_l),    # load game
            (4, pygame.K_s),    # view high scores
            (6, pygame.K_c),    # view credits
            (8, pygame.K_q),    # quit
        ]
        for i, (base_idx, key) in enumerate(buttons):
            self.attach(
                fhomm.ui.IcnButton(loader, 'btnmain.icn', base_idx, key),
                Pos(8, 20 + 66*i),
            )

    def on_render(self, ctx):
        # print(f"clip: {ctx._image.get_clip()}")
        self.bg_image.render(ctx)
