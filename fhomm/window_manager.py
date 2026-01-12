from collections import defaultdict
from contextlib import contextmanager
import traceback

import pygame

from fhomm.render import Pos, Size, Rect
import fhomm.handler
import fhomm.ui


def defaultdefaultdict():
    return defaultdict(defaultdefaultdict)


class WindowManager(fhomm.ui.Container):

    _SHADOW_OFFSET = Pos(16, 16)

    def __init__(self, screen, palette, toolkit, main_handler, fps_limit=30):
        super().__init__(Size(screen.get_width(), screen.get_height()))

        self.screen = screen
        self.palette = palette
        self.toolkit = toolkit
        self.fps_limit = fps_limit

        self.screen_ctx = fhomm.render.Context(screen)
        self.bg_captures = []
        self.running = False
        self.last_exception = None

        self.state = defaultdefaultdict()

        self.show_fps = False
        self._bg_fps = None

        self.show(main_handler, Pos(0, 0))

    def attach(self, element, pos, key=None):
        raise Exception("Elements should not be attached to window manager directly!")

    def detach(self, element):
        raise Exception("Elements should not be detached from window manager directly!")

    def show(self, element, screen_pos):
        super().attach(element, screen_pos)

        self._capture_background(element, screen_pos)

        element.dirty()

    def close_active(self):
        child = self.active_child()
        super().detach(child.element)

        self.bg_captures.pop().render(self.screen_ctx, child.relpos)

    def _capture_background(self, element, screen_pos):
        if element.size.w < self.screen.get_width() or \
           element.size.h < self.screen.get_height():
            shadow = True
            capture_size = Size(
                element.size.w + WindowManager._SHADOW_OFFSET.x,
                element.size.h + WindowManager._SHADOW_OFFSET.y,
            )
            bg_rect = Rect.of(capture_size, screen_pos)
        else:
            shadow = False
            bg_rect = Rect.of(element.size, screen_pos)

        background = self.screen_ctx.capture(bg_rect)
        self.bg_captures.append(background)

        if shadow:
            self._cast_shadow(background, bg_rect)

    def _cast_shadow(self, background, rect):
        img_shadow = fhomm.render.Context.make_shadow_image(rect.size)

        bg_copy = self.screen_ctx.copy_image_for_shadow(background)
        img_shadow.render(bg_copy.get_context(), WindowManager._SHADOW_OFFSET)
        bg_copy.render(self.screen_ctx, rect.pos)

    def active_child(self):
        return self.child_slots[-1]

    def render(self, ctx, state, force=True): # False
        return self.render_child(self.active_child(), ctx, state, force)

    def render_fps(self, ctx, dt):
        fps = 0 if dt == 0 else 1000 // dt
        fps_text = str(fps)

        font = self.toolkit.get_font()
        layout = font.layout_text(fps_text)
        size = font.measure_layout(layout)
        pos = Pos(0, 0)

        if self._bg_fps is not None:
            self._bg_fps.render(ctx, pos)

        self._bg_fps = ctx.capture(Rect.of(size, pos))

        font.draw_layout(ctx, layout, pos)

    def handle(self, state, event):
        # kind of has to be here to always react
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_F1:
                return fhomm.handler.CMD_TOGGLE_DEBUG_UI_RENDER

            elif event.key == pygame.K_F2:
                return fhomm.handler.CMD_TOGGLE_DEBUG_UI_EVENTS

            elif event.key == pygame.K_F3:
                return fhomm.handler.CMD_TOGGLE_FPS

            elif event.key == pygame.K_F4:
                return fhomm.handler.CMD_TOGGLE_FULLSCREEN

            elif event.key == pygame.K_q and event.mod & pygame.KMOD_CTRL:
                return fhomm.handler.CMD_QUIT # DEBUG: fast quit

        cmd = self.handle_by_child(self.active_child(), state, event)
        if cmd is not None:
            return cmd

        return self.on_event(state, event)

    def on_event(self, state, event):
        if event.type == pygame.QUIT:
            return fhomm.handler.CMD_QUIT

    def __call__(self):
        self.run_event_loop()

    def run_event_loop(self):
        self.clock = pygame.time.Clock()

        self.last_exception = None

        self.running = True
        while self.running:
            self.event_loop_step()

        pygame.quit()

    # having this as a separate method helps with autoreload
    def event_loop_step(self):
        with self.logging_just_once():
            for event in pygame.event.get():
                one_or_more_cmd = self.handle(self.state, event)
                if one_or_more_cmd:
                    self.run_commands(one_or_more_cmd)

            if self.render(self.screen_ctx, self.state):
                # print("flippin")
                pygame.display.flip()

            dt = self.clock.tick(self.fps_limit)

            if self.show_fps:
                self.render_fps(self.screen_ctx, dt)

            # TODO: for now no way to move it to on_event, as a child handling
            # on tick will prevent palette from cycling a way to solve it may
            # be by re-thinking the short-circuit on first returned command
            if self.palette.update_tick(dt):
                self.screen.set_palette(self.palette.palette)

            self.post_tick_event(dt)

    @contextmanager
    def logging_just_once(self):
        try:
            yield
            self.last_exception = None
        except Exception as e:
            if self.last_exception is None:
                traceback.print_exc()

            self.last_exception = e

    def post_tick_event(self, dt):
        pygame.event.post(pygame.event.Event(fhomm.handler.EVENT_TICK, dt=dt))

    def post_close_event(self):
        pygame.event.post(pygame.event.Event(fhomm.handler.EVENT_WINDOW_CLOSED))

    def run_commands(self, one_or_more_cmd):
        if isinstance(one_or_more_cmd, fhomm.handler.Command):
            self.run_command(one_or_more_cmd)

        else:
            for cmd in one_or_more_cmd:
                self.run_command(cmd)

    def run_command(self, command):
        # TODO: table-based dispatch
        if command.code == fhomm.handler.QUIT:
            self.running = False

        elif command.code == fhomm.handler.IGNORE:
            pass

        elif command.code == fhomm.handler.TOGGLE_DEBUG_UI_RENDER:
            fhomm.ui.DEBUG_RENDER = not fhomm.ui.DEBUG_RENDER
            self.active_child().element.dirty()

        elif command.code == fhomm.handler.TOGGLE_DEBUG_UI_EVENTS:
            fhomm.ui.DEBUG_EVENTS = not fhomm.ui.DEBUG_EVENTS

        elif command.code == fhomm.handler.TOGGLE_FPS:
            self.show_fps = not self.show_fps

        elif command.code == fhomm.handler.TOGGLE_FULLSCREEN:
            pygame.display.toggle_fullscreen()

        elif command.code == fhomm.handler.SHOW:
            self.show(**command.kwargs)

        elif command.code == fhomm.handler.CLOSE:
            self.close_active()
            self.post_close_event()

        elif command.code == fhomm.handler.UPDATE:
            update(self.state, command.kwargs['ks'], command.kwargs['fn'])

        else:
            print(f"unknown command: {command}")


def todict(m):
    return {
        k: todict(v) if isinstance(v, defaultdict) else v
        for k, v in m.items()
    }


def update(m, ks, fn):
    import yaml
    print(f"update: {ks}\n{yaml.dump(todict(m))}")

    for k in ks[:-1]:
        m = m[k]
    k = ks[-1]
    m[k] = fn(m[k])

    # print(f"after update: {ks}\n{yaml.dump(todict(t))}")
