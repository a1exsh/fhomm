import pygame

import fhomm.render
from fhomm.render import Pos


class PygameLoader(object):
    def __init__(self, loader, pal_name):
        self.loader = loader
        self.palette = self.load_palette(pal_name)

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
        img = self.make_image(bmp.data, bmp.width, bmp.height)
        return fhomm.render.Image(img)

    def load_sprite(self, icn_name, idx):
        s = self.loader.load_icn(icn_name)[idx]
        img = self.make_image(s.data, s.width, s.height)
        img.set_colorkey(0)
        return fhomm.render.Sprite(img, Pos(s.offx, s.offy))

    def make_image(self, data, width, height):
        img = pygame.image.frombuffer(data, (width, height), 'P')
        img.set_palette(self.palette)
        return img
