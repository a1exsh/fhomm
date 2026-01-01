from collections import namedtuple
from contextlib import AbstractContextManager

import pygame

import fhomm.palette

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

    def get_context(self):
        return Context(self._img)

    def render(self, ctx, pos=Pos(0, 0)):
        ctx.blit(self, pos)


class Sprite(Image):
    def __init__(self, img, offset):
        super().__init__(img)
        self._offset = offset

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
