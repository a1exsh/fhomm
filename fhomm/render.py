from collections import namedtuple
from contextlib import AbstractContextManager

import pygame

import fhomm.palette
import fhomm.resource.bmp
import fhomm.resource.icn

Dim = namedtuple('Dim', ['w', 'h']) # TODO: rename to Size


class Pos(namedtuple('Pos', ['x', 'y'])):
    __slots__ = ()

    def offset(self, relpos):
        return Pos(self.x + relpos.x, self.y + relpos.y)


# TODO: go back to (x, y, w, h), compatible with pygame's representation
class Rect(namedtuple('Rect', ['dim', 'pos'], defaults=[Pos(0, 0)])):
    __slots__ = ()

    @classmethod
    def of(cls, x, y, w, h):
        return cls(Dim(w, h), Pos(x, y))

    def to_pygame(self):
        return (self.x, self.y, self.w, self.h)

    @property
    def x(self):
        return self.pos.x

    @property
    def y(self):
        return self.pos.y

    @property
    def w(self):
        return self.dim.w

    @property
    def h(self):
        return self.dim.h

    @property
    def top(self):
        return self.pos.y

    @property
    def left(self):
        return self.pos.x

    @property
    def bottom(self):
        return self.pos.y + self.dim.h

    @property
    def right(self):
        return self.pos.x + self.dim.w

    def offset(self, relpos):
        return Rect(self.dim, self.pos.offset(relpos))

    def contains(self, pos):
        return (
            self.left <= pos.x and pos.x <= self.right and
            self.top  <= pos.y and pos.y <= self.bottom
        )


class Image(object):
    def __init__(self, img):
        self._img = img
        self.dim = Dim(img.get_width(), img.get_height())

    @classmethod
    def from_bmp(cls, bmp, palette):
        return cls(cls.make_surface(bmp.data, bmp.width, bmp.height, palette))

    @classmethod
    def make_surface(cls, data, width, height, palette):
        img = pygame.image.frombuffer(data, (width, height), 'P')
        img.set_palette(palette)
        return img

    def get_context(self):
        return Context(self._img)

    def render(self, ctx, pos=Pos(0, 0)):
        ctx.blit(self, pos)


class Sprite(Image):
    def __init__(self, img, offset):
        super().__init__(img)
        self._offset = offset

    @classmethod
    def from_icn_sprite(cls, icn_sprite, palette):
        img = Image.make_surface(
            icn_sprite.data,
            icn_sprite.width,
            icn_sprite.height,
            palette,
        )
        img.set_colorkey(0)
        return cls(img, Pos(icn_sprite.offx, icn_sprite.offy))

    def render(self, ctx, pos=Pos(0, 0)):
        super().render(ctx, Pos(pos.x + self._offset.x, pos.y + self._offset.y))


class Context(object):
    def __init__(self, img):
        self._image = img

    def make_image(self, dim):
        img = pygame.Surface(dim, depth=8)
        img.set_palette(self._image.get_palette())
        return Image(img)

    def copy_image_for_shadow(self, source):
        img = pygame.Surface(source.dim, depth=8)
        # TODO: get the pre-made shadow-safe palette from the Palette object
        img.set_palette(fhomm.palette.make_safe_for_shadow(self._image.get_palette()))
        img.blit(source._img, (0, 0)) # area?
        return Image(img)

    @classmethod
    def make_shadow_image(cls, dim):
        img = pygame.Surface(dim)
        img.set_alpha(96)
        return Image(img)

    def draw_rect(self, color, rect, width=0):
        pygame.draw.rect(self._image, color, rect.to_pygame(), width)

    def blit(self, source, pos=Pos(0, 0), rect=None):
        self._image.blit(
            source._img,
            pos,
            area=(None if rect is None else rect.to_pygame()),
        )

    def capture(self, rect):
        img = self.make_image(rect.dim)
        img.get_context().blit(Image(self._image), (0, 0), rect)
        return img

    def restrict(self, rect):
        # print(f"restricting to {rect}")
        return RestrictingContext(self, rect)


class RestrictingContext(Context):
    def __init__(self, ctx, rect):
        super().__init__(ctx._image)
        self._restriction = rect

    def __enter__(self):
        self._old_clip = self._image.get_clip()
        self._image.set_clip(self._restriction.to_pygame())
        return self

    def __exit__(self, *args, **kwargs):
        self._image.set_clip(self._old_clip)

    def draw_rect(self, color, rect, width=0):
        super().draw_rect(color, rect.offset(self._restriction.pos), width)

    def blit(self, source, pos=Pos(0, 0), rect=None):
        super().blit(source, pos.offset(self._restriction.pos), rect=rect)

    def capture(self, rect):
        return super().capture(rect.offset(self._restriction.pos))

    def restrict(self, rect):
        # TODO: should also restrict width and height
        return super().restrict(rect.offset(self._restriction.pos))


class Font(object):
    def __init__(self, sprites):
        if len(sprites) != 96:
            raise Exception("The font ICN file must have 96 sprites in it.")

        self.sprites = sprites

    def draw_text(self, ctx, text, pos=Pos(0, 0)):
        for c in text:
            sprite = self.sprite[self.get_sprite_idx(c) or 0]
            sprite.render(ctx, pos)

            pos = pos.offset(Pos(sprite.dim.w, 0))

    def get_sprite_idx(self, c):
        i = int(c)
        if int('A') <= i and i <= int('Z'):
            return 33 + (i - int('A'))
