from collections import namedtuple

import pygame

import fhomm.render
from fhomm.render import Pos, Dim, Rect


class Element(object):
    def __init__(self):
        self.parent = None

        self.hovered = False
        # self._first_render = True
        self._dirty = True

    def measure(self, dim):
        print(f"{self} measured at {dim}")
        self.dim = dim
        self.rect = Rect(dim)

    def on_attach(self, parent):
        pass

    def dirty(self):
        self._dirty = True

    def render(self, ctx, force=False):
        # if self._first_render:
        #     self.on_first_render(ctx)
        #     self._first_render = False
        #     force = True

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
            return True         # rendered, tell to update the screen

        return False

    # def on_first_render(self, ctx):
    #     pass

    def on_render(self, ctx):
        pass

    def handle(self, event):
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


class Container(Element):

    class ChildSlot(namedtuple('ChildSlot', ['element', 'relpos'])):
        __slots__ = ()

        @property
        def relrect(self):
            return Rect(self.element.dim, self.relpos)

    def __init__(self):
        super().__init__()
        self.child_slots = []

    def attach(self, element, relpos):
        if element.parent is not None:
            raise Exception(f"The UI element {element} is already attached to {parent}!")

        element.parent = self
        element.on_attach(self)
        self.child_slots.append(Container.ChildSlot(element, relpos))

    def render(self, ctx, force=False):
        update = super().render(ctx, force)
        if update:
            force = True

        for child in self.child_slots:
            if self.render_child(child, ctx, force):
                update = True

        return update

    def render_child(self, child, ctx, force=False):
        child_rect = child.relrect.offset(self.rect.pos)
        with ctx.restrict(child_rect) as child_ctx:
            return child.element.render(child_ctx, force)

    def handle(self, event):
#        print(f"{self}.handle: {event}")

        # TODO: input focus?
        cmd = self.on_event(event)
        if cmd is not None:
            return cmd

        for child in self.child_slots:
            cmd = self.handle_by_child(child, event)
            if cmd is not None:
                return cmd

    def handle_by_child(self, child, event):
        # TODO: if is_mouse_event(event):
        if event.type == pygame.MOUSEMOTION:
            # print(f"{self}.handle MOUSEMOTION: {event}")
            cur_pos = Pos(event.pos[0], event.pos[1])
            old_pos = Pos(event.pos[0] - event.rel[0], event.pos[1] - event.rel[1])
            child_rect = child.relrect.offset(self.rect.pos)
            if child_rect.contains(cur_pos) or \
               child_rect.contains(old_pos):
                return child.element.handle(
                    translate_mouse_event(event, child.relpos),
                )
            # command from mouse motion is ignored for now
        else:
            return child.element.handle(event)


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


class WindowManager(Container):

    def __init__(self, main_handler):
        super().__init__()
        self.attach(main_handler, Pos(0, 0))

    def active_handler(self):
        return self.child_slots[-1]

    def render(self, ctx, force=False):
        return self.render_child(self.active_handler(), ctx, force)

    def handle(self, event):
        return self.handle_by_child(self.active_handler(), event)


# class BackgroundCapturingElement(Element):
#     def on_first_render(self, ctx):
#         self.capture_background(ctx)

#     def capture_background(self, ctx, rect=None):
#         # TODO: assert before first render?
#         if rect is None:
#             rect = self.rect
#         self._bg_captured = ctx.capture(rect)

#     def restore_background(self, ctx, pos=Pos(0, 0)):
#         self._bg_captured.render(ctx, pos)


class Window(Container):

    # class WindowContents(Container):
    #     pass

    def __init__(self, border_width=25):
        super().__init__()
        self.border_width = border_width
        self.container = Container()
        super().attach(self.container, Pos(border_width, border_width))

    def attach(self, element, relpos):
        self.container.attach(element, relpos)

    def measure(self, dim):
        super().measure(dim)
        self.container.measure(
            Dim(
                self.dim.w - 2*self.border_width,
                self.dim.h - 2*self.border_width,
            )
        )


# class ShadowCastingWindow(BackgroundCapturingElement):
#     def __init__(self, shadow_offset=Pos(16, 16)):
#         super().__init__()
#         self._shadow_offset = shadow_offset

#     def measure(self, dim):
#         self._content_dim = dim
#         shadow_dim = Dim(
#             dim.w + self._shadow_offset.x,
#             dim.h + self._shadow_offset.y,
#         )
#         super().measure(shadow_dim)

#     def on_first_render(self, ctx):
#         self.capture_background(ctx)

#         img_shadow = fhomm.render.Context.make_shadow_image(self._content_dim)

#         bg_copy = ctx.copy_image_for_shadow(self._bg_captured)
#         bg_copy.get_context().blit(img_shadow, self._shadow_offset)
#         bg_copy.render(ctx)

#     def on_render(self, ctx):
#         with ctx.restrict(Rect(self._content_dim)) as content_ctx:
#             self.on_render_content(content_ctx)

#     # def on_detach(self):
#     #     self.restore_background()


# class ContentClippingWindow(BackgroundCapturingElement):
#     def __init__(self, border_width=25):
#         super().__init__()
#         self._border_width = border_width

#     def measure(self, dim):
#         super().measure(dim)
#         self._clipping_rect = Rect.of(
#             self._border_width,
#             self._border_width,
#             dim.w - self._border_width,
#             dim.h - self._border_width,
#         )

#     def on_render(self, ctx):
#         with ctx.clip(self._clipping_rect) as clip_ctx:
#             self.on_render_content(clip_ctx)


class IcnButton(Element): #BackgroundCapturingElement
    def __init__(self, loader, icn_name, base_idx, hotkey=None):
        super().__init__()
        self.img = loader.load_sprite(icn_name, base_idx)
        self.img_pressed = loader.load_sprite(icn_name, base_idx + 1)
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
        # self.restore_background(ctx) # optional

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
