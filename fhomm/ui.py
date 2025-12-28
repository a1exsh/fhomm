from collections import namedtuple
import pygame

import fhomm.handler

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


# class Button(object):
#     def __init__(self, pos, img, img_pressed, hotkey=None):
#         self.pos = pos
#         self.img = img
#         self.img_pressed = img_pressed
#         self.hotkey = hotkey

#         self.rect = Rect(
#             self.pos.x,
#             self.pos.y,
#             self.img.get_width(),
#             self.img.get_height(),
#         )
#         self.is_pressed = False

#     # TODO: doesn't have to be screen, could be some random surface
#     def render(self, screen):
#         img = self.img_pressed if self.is_pressed else self.img
#         img.render(screen, self.pos)


class IcnButton(fhomm.handler.Handler):
    def __init__(self, screen, loader, pos, icn_name, base_idx, hotkey=None):
        super().__init__(screen, loader)
        self.pos = pos
        self.img = self.loader.load_sprite(icn_name, base_idx)
        self.img_pressed = self.loader.load_sprite(icn_name, base_idx + 1)
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

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == self.hotkey:
                print(f"hotkey: {self.hotkey}")

        elif event.type == pygame.MOUSEMOTION:
            #print(event)
            mouse_pos = Pos(event.pos[0], event.pos[1])
            if pos_in_rect(mouse_pos, self.rect):
                if self.set_pressed():
                    self.needs_render = True
            else:
                if self.set_released():
                    self.needs_render = True

    def on_render(self):
        img = self.img_pressed if self.is_pressed else self.img
        img.render(self.screen, self.pos)
        

def pos_in_rect(pos, rect):
    return \
        rect.x <= pos.x and pos.x <= (rect.x + rect.w) and \
        rect.y <= pos.y and pos.y <= (rect.y + rect.h)
