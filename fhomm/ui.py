from collections import namedtuple
import pygame

import fhomm.handler

Pos = namedtuple('Pos', ['x', 'y'])
Rect = namedtuple('Rect', ['x', 'y', 'w', 'h'])


class Handler(object):
    def __init__(self, screen, loader):
        self.screen = screen
        self.loader = loader
        self.children = []
        self.hovered = False
        self._dirty = True

    def dirty(self):
        self._dirty = True

    def render(self, force=False):
        flip = False

        if self._dirty or force:
            # print(f"needs render: {self}")
            self.on_render()
            # DEBUG
            if self.hovered:
                pygame.draw.rect(self.screen, 228, self.rect, 1)
            # DEBUG
            self._dirty = False
            flip = True
            force = True

        for child in self.children:
            if child.render(force):
                flip = True

        return flip

    def on_render(self):
        pass

    def handle(self, event):
#        print(f"{self}.handle: {event}")

        if event.type == pygame.MOUSEMOTION:
            # print(f"{self}.handle MOUSEMOTION: {event}")
            cur_mouse_pos = Pos(event.pos[0], event.pos[1])
            old_mouse_pos = Pos(event.pos[0] - event.rel[0], event.pos[1] - event.rel[1])
            for child in self.children:
                if pos_in_rect(cur_mouse_pos, child.rect) or \
                   pos_in_rect(old_mouse_pos, child.rect):
                    child.handle(event)
        else:
            for child in self.children:
                cmd = child.handle(event)
                if cmd is not None:
                    #print(cmd)
                    return cmd

        return self.on_event(event)

    def on_event(self, event):
        #print(f"{self}.on_event: {event}")

        if event.type == pygame.MOUSEMOTION:
            mouse_pos = Pos(event.pos[0], event.pos[1])
            if pos_in_rect(mouse_pos, self.rect):
                old_hovered, self.hovered = self.hovered, True
            else:
                old_hovered, self.hovered = self.hovered, False
            if old_hovered != self.hovered:
                self.dirty()    # DEBUG
                if self.hovered:
                    self.on_mouse_enter()
                else:
                    self.on_mouse_leave()

    def on_mouse_enter(self):
        pass

    def on_mouse_leave(self):
        pass


class IcnButton(Handler):
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

    def on_render(self):
        img = self.img_pressed if self.is_pressed else self.img
        img.render(self.screen, self.pos)

    def on_mouse_enter(self):
        self.is_pressed = True
        self.dirty()

    def on_mouse_leave(self):
        self.is_pressed = False
        self.dirty()

    # def on_event(self, event):
    #     #print(f"IcnButton.on_event: {event}")

    #     if event.type == pygame.KEYDOWN:
    #         if event.key == self.hotkey:
    #             print(f"hotkey: {self.hotkey}")
        

def pos_in_rect(pos, rect):
    return (
        rect.x <= pos.x and pos.x <= (rect.x + rect.w) and
        rect.y <= pos.y and pos.y <= (rect.y + rect.h)
    )
