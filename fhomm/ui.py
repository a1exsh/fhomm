from collections import namedtuple

Pos = namedtuple('Pos', ['x', 'y'])
Rect = namedtuple('Rect', ['x', 'y', 'w', 'h'])


class Image(object):
    def __init__(self, img):
        self.img = img

    def render(self, screen, pos):
        screen.blit(self.img, pos)

    def get_width(self):
        return self.img.get_width()

    def get_height(self):
        return self.img.get_height()


class Sprite(Image):
    def __init__(self, img, offx, offy):
        super().__init__(img)
        self.offx = offx
        self.offy = offy

    def render(self, screen, pos):
        screen.blit(self.img, (pos.x + self.offx, pos.y + self.offy))


class Button(object):
    def __init__(self, pos, img, img_pressed, hotkey=None):
        self.pos = pos
        self.img = img
        self.img_pressed = img_pressed
        self.hotkey = hotkey

        self.rect = Rect(
            self.pos.x,
            self.pos.y,
            self.img.get_width(),
            self.img.get_height(),
        )
        self.is_pressed = False

    def set_pressed(self):
        changed = not self.is_pressed
        self.is_pressed = True
        return changed

    def set_released(self):
        changed = self.is_pressed
        self.is_pressed = False
        return changed

    # TODO: doesn't have to be screen, could be some random surface
    def render(self, screen):
        img = self.img_pressed if self.is_pressed else self.img
        img.render(screen, self.pos)


def pos_in_rect(pos, rect):
    return \
        rect.x <= pos.x and pos.x <= (rect.x + rect.w) and \
        rect.y <= pos.y and pos.y <= (rect.y + rect.h)
