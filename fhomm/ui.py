from collections import namedtuple

import pygame

from fhomm.render import Pos, Dim, Rect
import fhomm.handler
import fhomm.render

DEBUG_RENDER = False
DEBUG_EVENTS = False


def is_mouse_event(event):
    return event.type in [
        pygame.MOUSEMOTION,
        pygame.MOUSEBUTTONDOWN,
        pygame.MOUSEBUTTONUP,
        pygame.MOUSEWHEEL,
    ]


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
    def __init__(self):
        self.parent = None

        self.hovered = False
        # self._first_render = True
        self._dirty = False

    def measure(self, dim):
        #print(f"{self} measured at {dim}")
        self.dim = dim
        self.rect = Rect(dim)

    def on_attach(self, parent):
        pass

    def on_detach(self):
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

            if DEBUG_RENDER and self.hovered:
                ctx.draw_rect(228, self.rect, 1)

            return True         # rendered, tell to update the screen

        return False

    # def on_first_render(self, ctx):
    #     pass

    def on_render(self, ctx):
        pass

    def handle(self, event):
        if DEBUG_EVENTS and event.type != fhomm.handler.EVENT_TICK:
            print(f"{self}.handle: {event}")

        return self.on_event(event)

    # on_event is low level, better define one of the more specific on_XXX
    def on_event(self, event):
        #print(f"{self}.on_event: {event}")

        if event.type == fhomm.handler.EVENT_TICK:
            return self.on_tick(event.dt)

        elif is_mouse_event(event):
            return self.handle_mouse_event(event)

        elif event.type == pygame.KEYDOWN:
            return self.on_key_down(event.key)

        elif event.type == pygame.KEYUP:
            return self.on_key_up(event.key)

        elif event.type == pygame.QUIT:
            return self.on_quit()

    def handle_mouse_event(self, event):
        pos = Pos(event.pos[0], event.pos[1])

        if event.type == pygame.MOUSEMOTION:
            old, self.hovered = self.hovered, self.rect.contains(pos)
            if old != self.hovered:
                if DEBUG_RENDER:
                    self.dirty()

                if self.hovered:
                    self.on_mouse_enter() # no way to issue cmd for now
                else:
                    self.on_mouse_leave()

            relpos = Pos(event.rel[0], event.rel[1])
            return self.on_mouse_move(pos, relpos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            #print(f"mousedown: {event}")
            if event.button == 4 or event.button == 5:
                pass

            else:
                return self.on_mouse_down(pos, event.button)

        elif event.type == pygame.MOUSEBUTTONUP:
            #print(f"mouseup: {event}")
            if event.button == 4:
                return self.on_mouse_wheel(pos, 0, -1)

            elif event.button == 5:
                return self.on_mouse_wheel(pos, 0, 1)

            else:
                return self.on_mouse_up(pos, event.button)

        elif event.type == pygame.MOUSEWHEEL:
            print(f"mousewheel: {event}")
            return self.on_mouse_wheel(mouse_pos, event.x, event.y)

    def on_tick(self, dt):
        pass

    def on_mouse_enter(self):
        pass

    def on_mouse_leave(self):
        pass

    def on_mouse_move(self, pos, relpos):
        pass

    def on_mouse_down(self, pos, button):
        pass

    def on_mouse_up(self, pos, button):
        pass

    def on_mouse_wheel(self, pos, dx, dy):
        pass

    def on_key_down(self, key):
        pass

    def on_key_up(self, key):
        pass

    def on_quit(self):
        return fhomm.handler.CMD_IGNORE


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

    def detach(self, element):
        if self is not element.parent:
            raise Exception(f"The UI element {element} is not attached to {self}!")

        self.child_slots = [
            child
            for child in self.child_slots
            if element is not child.element
        ]
        element.on_detach()
        element.parent = None

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
        if is_mouse_event(event):
            cur_pos = Pos(event.pos[0], event.pos[1])
            if event.type == pygame.MOUSEMOTION:
                old_pos = Pos(
                    event.pos[0] - event.rel[0],
                    event.pos[1] - event.rel[1],
                )
            else:
                old_pos = None

            child_rect = child.relrect.offset(self.rect.pos)
            if child_rect.contains(cur_pos) or \
               (old_pos is not None and child_rect.contains(old_pos)):
                return child.element.handle(
                    translate_mouse_event(event, child.relpos),
                )

        else:
            return child.element.handle(event)


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


class ImgButton(Element):
    def __init__(self, img, action, hotkey=None):
        super().__init__()
        self.img = img
        self.action = action
        self.hotkey = hotkey

        self.is_pressed = False

        self.measure(self.img.dim)

    def on_render(self, ctx):
        self.img.render(ctx)

    def set_pressed(self):
        old, self.is_pressed = self.is_pressed, True
        return old != self.is_pressed

    def set_released(self):
        old, self.is_pressed = self.is_pressed, False
        return old != self.is_pressed

    def press(self):
        if self.set_pressed():
            self.dirty()

    def release(self, action=True):
        if self.set_released():
            self.dirty()
            if action:
                return self.action()

    def on_key_down(self, key):
        if key == self.hotkey:
            return self.press()

    def on_key_up(self, key):
        if key == self.hotkey:
            return self.release()

    def on_mouse_leave(self):
        self.release(action=False)

    def on_mouse_down(self, pos, button):
        # print(f"{self} mouse down: {pos} {button}")
        if button == 1:         # TODO: are there consts for this?
            return self.press()

    def on_mouse_up(self, pos, button):
        if button == 1:
            return self.release()


class IcnButton(ImgButton): #BackgroundCapturingElement
    def __init__(self, loader, icn_name, base_idx, action, hotkey=None):
        super().__init__(
            loader.load_sprite(icn_name, base_idx),
            action,
            hotkey=hotkey
        )
        self.img_pressed = loader.load_sprite(icn_name, base_idx + 1)

    def on_render(self, ctx):
        img = self.img_pressed if self.is_pressed else self.img
        img.render(ctx)


class ImgList(Element):

    Item = namedtuple('Item', ['img', 'text'])

    def __init__(self, dim, items, item_dim, item_pad=1):
        super().__init__()
        self.measure(dim)
        self.item_dim = item_dim
        self.item_pad = item_pad

        self.items = items

        self.scroll_idx = 0
        self.items_per_page = dim.h // (item_dim.h + item_pad)
        # TODO: allow for space between items?..
        self.list_pad = Dim(
            3,
            (dim.h - self.items_per_page*(item_dim.h + item_pad)) // 2,
        )

        self.tick = 0
        self.key_hold_ticks = 50
        self.key_hold_scroll_delta = None

    def on_render(self, ctx):
        for i in range(min(len(self.items), self.items_per_page)):
            img_item = self.items[self.scroll_idx + i].img
            img_item.render(
                ctx,
                Pos(
                    self.list_pad.w,
                    self.list_pad.h + (self.item_dim.h + self.item_pad)*i,
                )
            )

    def scroll(self, delta):
        max_scroll_idx = len(self.items) - self.items_per_page
        new = max(0, min(self.scroll_idx + delta, max_scroll_idx))
        old, self.scroll_idx = self.scroll_idx, new
        if old != self.scroll_idx:
            self.dirty()

    def on_mouse_wheel(self, pos, dx, dy):
        self.scroll(dy)

    def on_key_down(self, key):
        delta = None

        if key == pygame.K_DOWN:
            delta = 1

        elif key == pygame.K_UP:
            delta = -1

        if key == pygame.K_PAGEDOWN:
            delta = self.items_per_page

        elif key == pygame.K_PAGEUP:
            delta = -self.items_per_page

        if delta is not None and self.key_hold_scroll_delta is None:
            self.scroll(delta)
            self.ticks = 0
            self.key_hold_scroll_delta = delta

    def on_key_up(self, key):
        if key in [pygame.K_DOWN, pygame.K_UP, pygame.K_PAGEDOWN, pygame.K_PAGEUP]:
            self.key_hold_scroll_delta = None

    def on_tick(self, dt):
        if self.key_hold_scroll_delta is not None:
            self.tick += dt
            while self.tick >= self.key_hold_ticks:
                self.scroll(self.key_hold_scroll_delta)
                self.tick -= self.key_hold_ticks
