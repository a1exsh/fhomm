from collections import namedtuple

import pygame

from fhomm.render import Pos, Size, Rect
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
        self._dirty = False

    def measure(self, size):
        #print(f"{self} measured at {size}")
        self.size = size
        self.rect = Rect(size)

    def on_attach(self, parent):
        pass

    def on_detach(self):
        pass

    def dirty(self):
        self._dirty = True

    def render(self, ctx, force=False):
        if self._dirty:
            self._dirty = False
            force = True

        if force:
            self.on_render(ctx)

            if DEBUG_RENDER and self.hovered:
                ctx.draw_rect(228, self.rect, 1)

            return True         # rendered, tell to update the screen

        return False

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
            return Rect(self.element.size, self.relpos)

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


class Window(Container):
    def __init__(self, border_width):
        super().__init__()
        self.border_width = border_width
        self.container = Container()
        super().attach(self.container, Pos(border_width, border_width))

    def attach(self, element, relpos):
        self.container.attach(
            element,
            relpos.offset(Pos(-self.border_width, -self.border_width)),
        )

    def measure(self, size):
        super().measure(size)
        self.container.measure(
            Size(
                self.size.w - 2*self.border_width,
                self.size.h - 2*self.border_width,
            )
        )


class Label(Element):
    def __init__(self, size, font, text):
        super().__init__()
        self.measure(size)
        self.font = font
        self.text = text

        text_size = font.measure_text(text)
        self.text_pos = Pos(
            (size.w - text_size.w) // 2,
            (size.h - text_size.h) // 2,
        )

    def on_render(self, ctx):
        self.font.draw_text(ctx, self.text, self.text_pos)


class ImgButton(Element):
    def __init__(self, img, action, hotkey=None):
        super().__init__()
        self.img = img
        self.action = action
        self.hotkey = hotkey

        self.is_pressed = False

        self.measure(self.img.size)

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

    def __init__(
            self,
            size,
            font,
            hl_font,
            items,
            item_size,
            item_vpad=1,
            text_hpad=4
    ):
        super().__init__()
        self.measure(size)

        self.font = font
        self.hl_font = hl_font

        self.item_size = item_size
        self.item_vpad = item_vpad
        self.text_hpad = text_hpad

        self.items = items

        self.selected_idx = None
        self.scroll_idx = 0
        self.items_per_page = size.h // (item_size.h + item_vpad)

        self.list_pad = Size(
            3,
            (size.h - self.items_per_page*(item_size.h + item_vpad)) // 2,
        )

        self._bg_capture = None

        self.tick = 0
        self.key_hold_ticks = 50
        self.key_hold_delta = None

    def on_render(self, ctx):
        if self._bg_capture is None:
            self._bg_capture = ctx.capture(self.rect)
        else:
            self._bg_capture.render(ctx)

        for i in range(min(len(self.items), self.items_per_page)):
            item_idx = self.scroll_idx + i
            item = self.items[item_idx]
            img_pos = Pos(
                self.list_pad.w,
                self.list_pad.h + (self.item_size.h + self.item_vpad)*i,
            )
            item.img.render(ctx, img_pos)

            text_pos = Pos(
                img_pos.x + self.item_size.w + self.text_hpad,
                img_pos.y,
            )
            bound_rect = Rect(
                Size(self.rect.right - text_pos.x, self.item_size.h),
                text_pos,
            )
            if DEBUG_RENDER:
                ctx.draw_rect(240, bound_rect, width=1)

            font = self.hl_font if item_idx == self.selected_idx else self.font
            text_size = font.measure_multiline_text(item.text, bound_rect)

            # center vertically before actually drawing the item text
            text_rect = Rect(
                text_size,
                Pos(
                    text_pos.x,
                    text_pos.y + (self.item_size.h - text_size.h) // 2,
                ),
            )
            if DEBUG_RENDER:
                ctx.draw_rect(224, text_rect, width=1)

            font.draw_multiline_text(ctx, item.text, text_rect)

    def set_scroll_idx(self, idx):
        old, self.scroll_idx = self.scroll_idx, idx
        if old != self.scroll_idx:
            self.dirty()

    def get_max_scroll_idx(self):
        return len(self.items) - self.items_per_page

    def scroll_by(self, delta):
        self.set_scroll_idx(
            max(0, min(self.scroll_idx + delta, self.get_max_scroll_idx()))
        )

    def set_selected_idx(self, idx):
        old, self.selected_idx = self.selected_idx, idx
        if old != self.selected_idx:
            self.dirty()

    def move_selection_by(self, delta):
        self.set_selected_idx(
            max(0, min(self.selected_idx + delta, len(self.items) - 1))
        )
        if self.selected_idx < self.scroll_idx:
            self.set_scroll_idx(self.selected_idx)

        elif self.selected_idx >= self.scroll_idx + self.items_per_page:
            self.set_scroll_idx(self.selected_idx - self.items_per_page + 1)

    def on_key_down(self, key):
        if not self.items:      # no selection in an empty list
            return

        delta = None

        if key == pygame.K_UP:
            delta = -1

        elif key == pygame.K_DOWN:
            delta = 1

        elif key == pygame.K_PAGEUP:
            delta = -self.items_per_page

        elif key == pygame.K_PAGEDOWN:
            delta = self.items_per_page

        elif key == pygame.K_HOME:
            self.set_selected_idx(0)
            self.set_scroll_idx(0)

        elif key == pygame.K_END:
            self.set_selected_idx(len(self.items) - 1)
            self.set_scroll_idx(self.get_max_scroll_idx())

        if delta is not None and self.key_hold_delta is None:
            if self.selected_idx is None:
                self.set_selected_idx(0)
            else:
                self.move_selection_by(delta)

            self.tick = -250    # start repeating after a short delay 
            self.key_hold_delta = delta

    def on_key_up(self, key):
        if key in [pygame.K_DOWN, pygame.K_UP, pygame.K_PAGEDOWN, pygame.K_PAGEUP]:
            self.key_hold_delta = None

    def on_tick(self, dt):
        if self.key_hold_delta is not None:
            self.tick += dt
            while self.tick >= self.key_hold_ticks:
                self.move_selection_by(self.key_hold_delta)
                self.tick -= self.key_hold_ticks

    def on_mouse_down(self, pos, button):
        if button == 1:
            visible_idx = (
                (pos.y - self.list_pad.h)
                //
                (self.item_size.h + self.item_vpad)
            )
            item_idx = self.scroll_idx + visible_idx
            last_visible_idx = min(
                self.scroll_idx + self.items_per_page,
                len(self.items),
            )
            if item_idx in range(last_visible_idx):
                self.set_selected_idx(item_idx)

    def on_mouse_wheel(self, pos, dx, dy):
        self.scroll_by(dy)
