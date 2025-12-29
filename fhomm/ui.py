from collections import namedtuple
import pygame

import fhomm.handler

Pos = namedtuple('Pos', ['x', 'y'])
Rect = namedtuple('Rect', ['x', 'y', 'w', 'h'])


class Element(object):
    def __init__(self, screen, loader):
        self.screen = screen
        self.loader = loader
        self.children = []
        self.hovered = False
        self._first_render = True
        self._dirty = False

    def attach(self, child):
        # TODO: assert not attached already?
        self.children.append(child)
        child.on_attach()

    def on_attach(self):
        pass

    def dirty(self):
        self._dirty = True

    def render(self, force=False):
        flip = False

        if self._first_render:
            self.on_first_render()
            self._first_render = False
            force = True

        if self._dirty:
            self._dirty = False
            force = True

        if force:
            # print(f"needs render: {self}")
            self.on_render()
            # DEBUG
            if self.hovered:
                pygame.draw.rect(self.screen, 228, self.rect, 1)
            # DEBUG
            flip = True

        for child in self.children:
            if child.render(force):
                flip = True

        return flip

    def on_first_render(self):
        pass

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


class BackgroundCapturingElement(Element):
    def on_first_render(self):
        self.capture_background()

    def capture_background(self, rect=None):
        # TODO: assert before first render?
        if rect is None:
            rect = self.rect

        self.captured_bg = pygame.Surface((rect.w, rect.h), depth=8)
        self.captured_bg.set_palette(self.screen.get_palette())
        self.captured_bg.blit(self.screen, (0, 0), area=rect)

    def restore_background(self, pos=None):
        if pos is None:
            pos = Pos(self.rect.x, self.rect.y)

        self.screen.blit(self.captured_bg, pos)


class ShadowCastingWindow(BackgroundCapturingElement):
    def on_first_render(self):
        shadow_pos = Pos(16, 16)
        bg_area = Rect(
            self.rect.x,
            self.rect.y,
            self.rect.w + shadow_pos.x,
            self.rect.h + shadow_pos.y,
        )
        self.capture_background(rect=bg_area)

        bg_copy = pygame.Surface((bg_area.w, bg_area.h), depth=8)
        # TODO: get the pre-made shadow-safe palette from the Palette object
        bg_copy.set_palette(fhomm.palette.make_safe_for_shadow(self.screen.get_palette()))
        bg_copy.blit(self.captured_bg, (0, 0))

        shadow = pygame.Surface((self.rect.w, self.rect.h))
        shadow.set_alpha(96)
        bg_copy.blit(shadow, shadow_pos)

        self.screen.blit(bg_copy, (self.rect.x, self.rect.y))

    def on_detach(self):
        self.restore_background()


class IcnButton(BackgroundCapturingElement):
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
        self.restore_background() # optional

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
