from collections import namedtuple

import pygame

import fhomm.palette
import fhomm.resource.bmp
import fhomm.resource.icn

# module=
Size = namedtuple('Size', ['w', 'h'])


class Pos(namedtuple('Pos', ['x', 'y'])):
    __slots__ = ()

    def offset(self, relpos):
        return Pos(self.x + relpos.x, self.y + relpos.y)


class Rect(namedtuple('Rect', ['x', 'y', 'w', 'h'])):
    __slots__ = ()

    @classmethod
    def of(cls, size, pos=Pos(0, 0)):
        return cls(pos.x, pos.y, size.w, size.h)

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
        return self.y + self.h

    @property
    def right(self):
        return self.x + self.w

    def offset(self, relpos):
        return Rect(self.x + relpos.x, self.y + relpos.y, self.w, self.h)

    # TODO: __contains__
    def contains(self, pos):
        return (
            pos.x in range(self.left, self.right) and
            pos.y in range(self.top, self.bottom)
        )


class Image(object):
    def __init__(self, img):
        self._img = img
        self.size = Size(img.get_width(), img.get_height())

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
        self.offset = offset

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
        super().render(ctx, Pos(pos.x + self.offset.x, pos.y + self.offset.y))


class Context(object):
    def __init__(self, img):
        self._image = img

    def make_image(self, size):
        img = pygame.Surface(size, depth=8)
        img.set_palette(self._image.get_palette())
        return Image(img)

    def copy_image_for_shadow(self, source):
        img = pygame.Surface(source.size, depth=8)
        # TODO: get the pre-made shadow-safe palette from the Palette object
        img.set_palette(fhomm.palette.make_safe_for_shadow(self._image.get_palette()))
        img.blit(source._img, (0, 0)) # area?
        return Image(img)

    @classmethod
    def make_shadow_image(cls, size):
        img = pygame.Surface(size)
        img.set_alpha(96)
        return Image(img)

    def draw_rect(self, color, rect, width=0):
        pygame.draw.rect(self._image, color, rect, width)

    def blit(self, source, pos=Pos(0, 0), rect=None):
        self._image.blit(source._img, pos, area=rect)

    def capture(self, rect):
        img = self.make_image(rect.size)
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
        self._image.set_clip(self._restriction)
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


class NoopContext(Context):
    def __init__(self):
        super().__init__(None)

    def draw_rect(self, *args, **kwargs):
        pass

    def blit(self, *args, **kwargs):
        pass

    def capture(self):
        return self.make_image(Size(0, 0))

    def restrict(self, *args, **kwargs):
        return self


class Font(object):
    def __init__(self, sprites, baseline, space_width):
        if len(sprites) != 96:
            raise Exception("The font ICN file must have 96 sprites in it.")

        self.sprites = sprites
        self.baseline = baseline
        self.space_width = space_width

        self.height = self.baseline + max(s.offset.y + s.size.h for s in sprites)

    def get_height(self):
        return self.height

    # TODO:
    # layout -> measure
    # layout -> draw
    def measure_text(self, text):
        return self.draw_text(NoopContext(), text)

    def draw_text(self, ctx, text, top_left=Pos(0, 0)):
        # input pos is the top-left corner, but each sprite has an offset to
        # make glyphs align on the the baseline
        pos = Pos(top_left.x, top_left.y + self.baseline)

        for c in text:
            if c == ' ':
                pos = Pos(pos.x + self.space_width, pos.y)

            else:
                sprite = self.sprites[self.get_sprite_idx(c) or 0]
                sprite.render(ctx, pos)

                pos = Pos(pos.x + sprite.size.w + 1, pos.y)

        width = pos.x - top_left.x
        if len(text) > 0:
            width -= 1          # account for space between glyphs

        return Size(width, self.baseline)

    def measure_multiline_text(self, text, rect):
        return self.draw_multiline_text(NoopContext(), text, rect)

    # TOOD: line spacing
    def draw_multiline_text(self, ctx, text, rect):
        maxx = rect.x
        maxy = rect.y
        pos = rect.pos

        words = text.split(' ')
        for i, word in enumerate(words):
            word_size = self.measure_text(word)
            if i > 0:
                pos = Pos(pos.x + self.space_width, pos.y)

                if pos.x + word_size.w > rect.right: # line break
                    pos = Pos(rect.x, pos.y + self.height)
                    if pos.y > maxy:
                        maxy = pos.y

            self.draw_text(ctx, word, pos)

            pos = Pos(pos.x + word_size.w, pos.y)
            if pos.x > maxx:
                maxx = pos.x

        return Size(maxx - rect.x, maxy - rect.y + self.baseline)

    def get_sprite_idx(self, c):
        i = ord(c)
        if 0x20 < i and i <= 0x7f:
            return i - 0x20
