from collections import namedtuple

import pygame

import fhomm.render
from fhomm.render import Pos, Dim, Rect


class ChildSlot(namedtuple('ChildSlot', ['element', 'pos'])):
    __slots__ = ()

    @property
    def rect(self):
        return Rect(self.element.dim, self.pos)


def translate_mouse_event(event, child_pos):
    return pygame.event.Event(
        event.type,
        {
            **event.__dict__,
            'pos': (
                event.pos[0] - child_pos.x,
                event.pos[1] - child_pos.y,
            ),
        },
    )


class Element(object):
    def __init__(self, loader):
        self.loader = loader

        self.parent = None
        self.child_slots = []

        self.hovered = False
        self._first_render = True
        self._dirty = False

    def measure(self, dim):
        print(f"{self} measured at {dim}")
        self.dim = dim
        self.rect = Rect(dim)

    def attach(self, element, pos):
        if element.parent is not None:
            raise Exception(f"The UI element {element} is already attached to {parent}!")

        element.parent = self
        element.on_attach(self)
        self.child_slots.append(ChildSlot(element, pos))

    def on_attach(self, parent):
        pass

    def dirty(self):
        self._dirty = True

    def render(self, ctx, force=False):
        flip = False

        if self._first_render:
            self.on_first_render(ctx)
            self._first_render = False
            force = True

        if self._dirty:
            self._dirty = False
            force = True

        if force:
            # print(f"needs render: {self}")
            self.on_render(ctx)
            # DEBUG
            if self.hovered:
                ctx.draw_rect(228, self.rect, 1)
            # DEBUG
            flip = True

        for child in self.child_slots:
            with ctx.restrict(child.rect) as child_ctx:
                if child.element.render(child_ctx, force):
                    flip = True

        return flip

    def on_first_render(self, ctx):
        pass

    def on_render(self, ctx):
        pass

    def handle(self, event):
#        print(f"{self}.handle: {event}")

        if event.type == pygame.MOUSEMOTION:
            # print(f"{self}.handle MOUSEMOTION: {event}")
            cur_pos = Pos(event.pos[0], event.pos[1])
            old_pos = Pos(event.pos[0] - event.rel[0], event.pos[1] - event.rel[1])
            for child in self.child_slots:
                child_rect = child.rect
                if child_rect.contains(cur_pos) or \
                   child_rect.contains(old_pos):
                    cmd = child.element.handle(
                        translate_mouse_event(event, child.pos),
                    )
                    # command from mouse motion is ignored for now
        else:
            for child in self.child_slots:
                cmd = child.element.handle(event)
                if cmd is not None:
                    #print(cmd)
                    return cmd

        return self.on_event(event)

    def on_event(self, event):
        #print(f"{self}.on_event: {event}")

        if event.type == pygame.MOUSEMOTION:
            mouse_pos = Pos(event.pos[0], event.pos[1])
            old, self.hovered = self.hovered, self.rect.contains(mouse_pos)
            if old != self.hovered:
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
    def on_first_render(self, ctx):
        self.capture_background(ctx)

    def capture_background(self, ctx, rect=None):
        # TODO: assert before first render?
        if rect is None:
            rect = self.rect
        self._bg_captured = ctx.capture(rect)

    def restore_background(self, ctx, pos=Pos(0, 0)):
        ctx.blit(self._bg_captured, pos)


class ShadowCastingWindow(BackgroundCapturingElement):
    def __init__(self, loader, shadow_offset=Pos(16, 16)):
        super().__init__(loader)
        self._shadow_offset = shadow_offset

    def measure(self, dim):
        self._content_dim = dim
        shadow_dim = Dim(
            dim.w + self._shadow_offset.x,
            dim.h + self._shadow_offset.y,
        )
        super().measure(shadow_dim)

    def on_first_render(self, ctx):
        self.capture_background(ctx)

        img_shadow = fhomm.render.Context.make_shadow_image(self._content_dim)

        bg_copy = ctx.copy_image_for_shadow(self._bg_captured)
        bg_copy.get_context().blit(img_shadow, self._shadow_offset)
        ctx.blit(bg_copy)

    def on_render(self, ctx):
        with ctx.restrict(Rect(self._content_dim)) as content_ctx:
            self.on_render_content(content_ctx)

    # def on_detach(self):
    #     self.restore_background()


class ContentClippingWindow(BackgroundCapturingElement):
    def __init__(self, loader, border_width=25):
        super().__init__(loader)
        self._border_width = border_width

    def measure(self, dim):
        super().measure(dim)
        self._clipping_rect = Rect.of(
            self._border_width,
            self._border_width,
            dim.w - self._border_width,
            dim.h - self._border_width,
        )

    def on_render(self, ctx):
        with ctx.clip(self._clipping_rect) as clip_ctx:
            self.on_render_content(clip_ctx)


class IcnButton(BackgroundCapturingElement):
    def __init__(self, loader, icn_name, base_idx, hotkey=None):
        super().__init__(loader)
        self.img = self.loader.load_sprite(icn_name, base_idx)
        self.img_pressed = self.loader.load_sprite(icn_name, base_idx + 1)
        self.hotkey = hotkey
        self.is_pressed = False

        self.measure(self.img.dim)

    # def set_pressed(self):
    #     changed = not self.is_pressed
    #     self.is_pressed = True
    #     return changed

    # def set_released(self):
    #     changed = self.is_pressed
    #     self.is_pressed = False
    #     return changed

    def on_render(self, ctx):
        self.restore_background(ctx) # optional

        img = self.img_pressed if self.is_pressed else self.img
        img.render(ctx)

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
