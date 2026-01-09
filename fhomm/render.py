from collections import namedtuple

import pygame

import fhomm.palette
import fhomm.resource.bmp
import fhomm.resource.icn

# module=
Size = namedtuple('Size', ['w', 'h'])


class Pos(namedtuple('Pos', ['x', 'y'])):
    __slots__ = ()

    def moved_by(self, relpos):
        return Pos(self.x + relpos.x, self.y + relpos.y)


class Rect(namedtuple('Rect', ['x', 'y', 'w', 'h'])):
    __slots__ = ()

    @classmethod
    def of(cls, size, pos=Pos(0, 0)):
        return cls(pos.x, pos.y, size.w, size.h)

    @classmethod
    def ltrb(cls, left, top, right, bottom):
        return cls(left, top, right - left + 1, bottom - top + 1)

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

    def get_context(self):
        return Context(self._surface)

    def render(self, ctx, pos=Pos(0, 0)):
        ctx.blit(self, pos)


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
        super().render(ctx, Pos(pos.x + self.offset.x, pos.y + self.offset.y))


# TODO: with context(): => lock/release surface
class Context(object):
    def __init__(self, surface):
        self._surface = surface

    def make_image(self, size):
        surface = pygame.Surface(size, depth=8)
        surface.set_palette(self._surface.get_palette())
        return Image(surface)

    def copy_image_for_shadow(self, source):
        surface = pygame.Surface(source.size, depth=8)
        # TODO: get the pre-made shadow-safe palette from the Palette object
        surface.set_palette(fhomm.palette.make_safe_for_shadow(self._surface.get_palette()))
        surface.blit(source._surface, (0, 0)) # area?
        return Image(surface)

    @classmethod
    def make_shadow_image(cls, size):
        surface = pygame.Surface(size)
        surface.set_alpha(96)
        return Image(surface)

    def draw_rect(self, color, rect, width=0):
        pygame.draw.rect(self._surface, color, rect, width)

    def blit(self, source, pos=Pos(0, 0), rect=None):
        self._surface.blit(source._surface, pos, area=rect)

    def capture(self, rect):
        image = self.make_image(rect.size)
        image.get_context().blit(Image(self._surface), (0, 0), rect)
        return image

    def restrict(self, rect):
        # print(f"restricting to {rect}")
        return RestrictingContext(self, rect)


class RestrictingContext(Context):
    def __init__(self, ctx, rect):
        super().__init__(ctx._surface)
        self._restriction = rect

    def __enter__(self):
        self._old_clip = self._surface.get_clip()
        self._surface.set_clip(self._restriction)
        return self

    def __exit__(self, *args, **kwargs):
        self._surface.set_clip(self._old_clip)

    def draw_rect(self, color, rect, width=0):
        super().draw_rect(color, rect.moved_by(self._restriction.pos), width)

    def blit(self, source, pos=Pos(0, 0), rect=None):
        super().blit(source, pos.moved_by(self._restriction.pos), rect=rect)

    def capture(self, rect):
        return super().capture(rect.moved_by(self._restriction.pos))

    def restrict(self, rect):
        # TODO: should also restrict width and height
        return super().restrict(rect.moved_by(self._restriction.pos))


# class NoopContext(Context):
#     def __init__(self):
#         super().__init__(None)

#     def draw_rect(self, *args, **kwargs):
#         pass

#     def blit(self, *args, **kwargs):
#         pass

#     def capture(self):
#         return self.make_empty_image()

#     def restrict(self, *args, **kwargs):
#         return self

# halign values
LEFT = 0
CENTER = 1
RIGHT = 2
# valign values
TOP = 3
# CENTER
BOTTOM = 4

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

    @classmethod
    def align_vertically(cls, rect, height, align):
        if align == CENTER:
            return rect.y + max(0, (rect.h - height) // 2)

        elif align == BOTTOM:
            return rect.bottom - min(height, rect.h)

        else:
            # FIXME: log warn if != TOP
            return rect.y

    @classmethod
    def align_horizontally(cls, rect, width, align):
        if align == CENTER:
            return rect.x + max(0, (rect.w - width) // 2)

        elif align == RIGHT:
            return rect.right - min(width, rect.w)

        else:
            # FIXME: log warn if != LEFT
            return rect.x

    def draw_text(self, ctx, text, rect, halign=LEFT, valign=TOP):
        layout = self.layout_text(text)
        size = self.measure_layout(layout)
        self.draw_layout(
            ctx,
            layout,
            Pos(
                Font.align_horizontally(rect, size.w, halign),
                Font.align_vertically(rect, size.h, valign),
            ),
        )

    def draw_layout(self, ctx, layout, pos=Pos(0, 0)):
        for sprite in layout:
            sprite.render(ctx, pos)

    def draw_multiline_text(
            self, ctx, text, rect,
            halign=LEFT, valign=TOP, line_space=0
    ):
        lines = self.layout_multiline_text(text, rect)
        total_height = (self.height + line_space)*(len(lines) - 1) + self.baseline

        pos = Pos(rect.x, Font.align_vertically(rect, total_height, valign))

        for line in lines:
            word_sizes = [self.measure_layout(word) for word in line]
            total_width = sum(
                size.w
                for size in word_sizes
            ) + self.space_width*(len(line) - 1)

            pos = Pos(Font.align_horizontally(rect, total_width, halign), pos.y)

            for word, size in zip(line, word_sizes):
                self.draw_layout(ctx, word, pos)
                pos = Pos(pos.x + size.w + self.space_width, pos.y)

            pos = Pos(rect.x, pos.y + self.height + line_space)

    def layout_text(self, text):
        glyphs = []

        # make glyphs align on the the baseline
        pos = Pos(0, self.baseline - 1)

        for c in text:
            if c == ' ':
                pos = Pos(pos.x + self.space_width, pos.y)

            else:
                sprite = self.sprites[Font.get_sprite_idx(c) or 0]
                glyphs.append(sprite.moved_by(pos))

                pos = Pos(pos.x + sprite.size.w + 1, pos.y)

        # width = pos.x - top_left.x
        # if len(text) > 0:
        #     width -= 1          # account for extra space after the last glyph

        return glyphs

    def measure_layout(self, layout):
        if len(layout) > 0:
            rightmost_sprite = layout[-1]
            width = rightmost_sprite.offset.x + rightmost_sprite.size.w
        else:
            width = 0

        return Size(width, self.baseline)

    def layout_multiline_text(self, text, rect):
        lines = []              # each line is a list of words (layouts)
        current_line = None

        posx = rect.pos.x

        words = text.split(' ')
        for i, word in enumerate(words):
            word_layout = self.layout_text(word)
            word_size = self.measure_layout(word_layout)
            if i > 0:
                posx += self.space_width
                if posx + word_size.w > rect.right: # line break
                    posx = rect.pos.x
                    current_line = []
                    lines.append(current_line)

            else:
                current_line = []
                lines.append(current_line)

            current_line.append(word_layout)

            posx += word_size.w

        return lines

    @classmethod
    def get_sprite_idx(self, c):
        i = ord(c)
        if 0x20 < i and i <= 0x7f:
            return i - 0x20
