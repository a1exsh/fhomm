from fhomm.render import Pos, Size, TOP, LEFT, CENTER, RIGHT, BOTTOM


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
