import pygame

import fhomm.render
from fhomm.render import Pos


class PygameLoader(object):
    def __init__(self, loader, pal_name):
        self.loader = loader
        self.palette = self.load_palette(pal_name)

        self.big_font = None
        self.small_font = None

    def get_big_font(self):
        if self.big_font is None:
            self.big_font = self.load_font('font.icn', 10)

        return self.big_font

    def get_small_font(self):
        if self.small_font is None:
            self.small_font = self.load_font('smalfont.icn', 5)

        return self.small_font

    def load_palette(self, pal_name):
        pal = self.loader.load_pal(pal_name)
        return [
            (
                4*pal[i*3],
                4*pal[i*3+1],
                4*pal[i*3+2],
            )
            for i in range(256)
        ]

    def load_image(self, bmp_name):
        bmp = self.loader.load_bmp(bmp_name)
        return fhomm.render.Image.from_bmp(bmp, self.palette)

    def load_sprite(self, icn_name, idx):
        return fhomm.render.Sprite.from_icn_sprite(
            self.loader.load_icn(icn_name)[idx],
            self.palette,
        )

    def load_all_sprites(self, icn_name):
        return [
            fhomm.render.Sprite.from_icn_sprite(
                icn_sprite,
                self.palette,
            )
            for icn_sprite in self.loader.load_icn(icn_name)
        ]

    def load_font(self, icn_name, width):
        return fhomm.render.Font(self.load_all_sprites(icn_name), width)
