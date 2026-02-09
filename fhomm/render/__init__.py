from collections import namedtuple

import pygame

import fhomm.palette
import fhomm.resource.bmp
import fhomm.resource.icn

# halign values
LEFT = 0
CENTER = 1
RIGHT = 2
# valign values
TOP = 3
# CENTER
BOTTOM = 4


class Size(namedtuple('Size', ['w', 'h'], module='fhomm.render')):
    __slots__ = ()

    def __getstate__(self):
        return self._asdict()

    def __getnewargs__(self):
        return ()


class Pos(namedtuple('Pos', ['x', 'y'], module='fhomm.render')):
    __slots__ = ()

    def __getstate__(self):
        return self._asdict()

    def __getnewargs__(self):
        return ()

    def moved_by(self, relpos):
        return Pos(self.x + relpos.x, self.y + relpos.y)


class Rect(namedtuple('Rect', ['x', 'y', 'w', 'h'], module='fhomm.render')):
    __slots__ = ()

    def __getstate__(self):
        return self._asdict()

    def __getnewargs__(self):
        return ()

    @classmethod
    def of(cls, size, pos=Pos(0, 0)):
        return cls(pos.x, pos.y, size.w, size.h)

    @classmethod
    def ltrb(cls, left, top, right, bottom):
        return cls(left, top, right - left + 1, bottom - top + 1)

    @classmethod
    def from_pygame(cls, rect):
        return cls(rect.x, rect.y, rect.w, rect.h)

    @property
    def pos(self):
        return Pos(self.x, self.y)

    @property
    def size(self):
        return Size(self.w, self.h)

    @property
    def top(self):
        return self.y

    @property
    def left(self):
        return self.x

    @property
    def bottom(self):
        return self.y + self.h - 1

    @property
    def right(self):
        return self.x + self.w - 1

    def moved_by(self, relpos):
        return Rect(self.x + relpos.x, self.y + relpos.y, self.w, self.h)

    def intersected_by(self, rect):
        ret = Rect.ltrb(
            max(self.left,   rect.left),
            max(self.top,    rect.top),
            min(self.right,  rect.right),
            min(self.bottom, rect.bottom),
        )
        # print(f"{self}.intersected_by({rect}) => {ret}")
        return ret

    # TODO: __contains__
    def contains(self, pos):
        return (
            pos.x in range(self.left, self.right) and
            pos.y in range(self.top, self.bottom)
        )


class Image(object):

    def __init__(self, surface):
        self._surface = surface
        self.size = Size(surface.get_width(), surface.get_height())

    @classmethod
    def make_surface(cls, data, width, height, palette):
        surface = pygame.image.frombuffer(data, (width, height), 'P')
        surface.set_palette(palette)
        return surface

    @classmethod
    def from_bmp(cls, bmp, palette):
        return cls(cls.make_surface(bmp.data, bmp.width, bmp.height, palette))

    @classmethod
    def make_empty(cls):
        return Image(pygame.Surface((1, 1), depth=8))

    def make_copy(self):
        return Image(self._surface.copy())

    # def __enter__(self):
    #     return self.get_context()

    # def __exit__(self, *args, **kwargs):
    #     pass

    def get_context(self):
        return Context(self._surface)

    def render(self, ctx, pos=Pos(0, 0)):
        ctx.blit(self, pos)

    # pickling support: don't try to dump the surface
    def __getstate__(self):
        return dict(
            self.__dict__,
            _surface="pygame.Surface",
        )


class Sprite(Image):

    def __init__(self, surface, offset):
        super().__init__(surface)
        self.offset = offset

    @classmethod
    def from_icn_sprite(cls, icn_sprite, palette):
        surface = Image.make_surface(
            icn_sprite.data,
            icn_sprite.width,
            icn_sprite.height,
            palette,
        )
        surface.set_colorkey(0)
        return cls(surface, Pos(icn_sprite.offx, icn_sprite.offy))

    @classmethod
    def from_image(cls, image, offset):
        return Sprite(image._surface, offset)

    @classmethod
    def make_empty(cls):
        surface = Image.make_empty()
        surface.set_colorkey(0)
        return Sprite(surface, Pos(0, 0))

    def make_copy(self):
        return Sprite(self._surface.copy(), self.offset)

    def moved_by(self, relpos):
        return Sprite(self._surface, self.offset.moved_by(relpos))

    def render(self, ctx, pos=Pos(0, 0)):
        super().render(ctx, pos.moved_by(self.offset))


class Context(object):
    def __init__(self, surface):
        self._surface = surface

    # TODO: lock/release surface
    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def make_image(self, size):
        surface = pygame.Surface(size, depth=8)
        surface.set_palette(self._surface.get_palette())
        return Image(surface)

    def copy_image_for_shadow(self, source):
        surface = pygame.Surface(source.size, depth=8)
        # TODO: get the pre-made shadow-safe palette from the Palette object
        surface.set_palette(
            fhomm.palette.make_safe_for_shadow(self._surface.get_palette())
        )
        surface.blit(source._surface, (0, 0)) # area?
        return Image(surface)

    @classmethod
    def make_shadow_image(cls, size):
        surface = pygame.Surface(size)
        surface.set_alpha(48)
        return Image(surface)

    def draw_rect(self, color, rect, width=0):
        pygame.draw.rect(self._surface, color, rect, width)

    def blit(self, source, pos=Pos(0, 0), rect=None):
        self._surface.blit(source._surface, pos, area=rect)

    def capture(self, rect):
        image = self.make_image(rect.size)
        image.get_context().blit(Image(self._surface), (0, 0), rect)
        return image

    def clip(self, rect):
        print(f"clip: {rect}")
        old = self._surface.get_clip()
        self._surface.set_clip(rect)
        return Rect(old.x, old.y, old.w, old.h)

    # def translate(self, pos):
    #     return TranslatingContext(self, pos)

    def restrict(self, rect):
        # print(f"restricting to {rect}")
        return RestrictingContext(self, rect)


# TODO: right now it mixes functions of both restricting and translating
class RestrictingContext(Context):
    def __init__(self, ctx, rect):
        parent_rect = Rect.from_pygame(ctx._surface.get_rect())
        # print(f"restricting: {parent_rect}, {rect}")
        # intersect to prevent "ValueError: subsurface rectangle outside surface area"
        super().__init__(
            ctx._surface.subsurface(rect.intersected_by(parent_rect))
        )

    # def __enter__(self):
    #     return self

    # def __exit__(self, *args, **kwargs):
    #     pass

    # def draw_rect(self, color, rect, width=0):
    #     super().draw_rect(color, rect.moved_by(self._rect.pos), width)

    # def blit(self, source, pos=Pos(0, 0), rect=None):
    #     super().blit(source, pos.moved_by(self._rect.pos), rect=rect)

    # def capture(self, rect):
    #     return super().capture(rect.moved_by(self._rect.pos))

    # def clip(self, rect):
    #     return super().clip(rect.moved_by(self._rect.pos))

    # def translate(self, pos):
    #     return super().translate(pos.moved_by(self._pos))

    # def restrict(self, rect):
    #     return super().restrict(
    #         rect.moved_by(self._rect.pos).intersected_by(self._rect)
    #     )


# class RestrictingContext(TranslatingContext):
#     def __init__(self, ctx, rect):
#         super().__init__(ctx, rect.pos)
#         self._rect = rect

#     def __enter__(self):
#         self._old_clip = self._wrapped.clip(Rect.of(self._rect.size))
#         return self

#     def __exit__(self, *args, **kwargs):
#         pass
#         self._wrapped.clip(
#             self._old_clip)
#         # .moved_by(Pos(-self._rect.pos.x, -self._rect.pos.y))
#         # )

#     # def restrict(self, rect):
#     #     return super().restrict(
#     #         rect.intersected_by(self._rect)
#     #     )
