from collections import namedtuple
from contextlib import contextmanager
import traceback
import yaml

import pygame

from fhomm import asdict
from fhomm.render import Pos, Size, Rect, Image
import fhomm.command
import fhomm.event
import fhomm.ui


class WindowManager(object):

    class WindowSlot(
        namedtuple(
            'WindowSlot',
            ['window', 'screen_pos', 'state_key', 'bg_capture'],
            module='fhomm.ui.WindowManager'
        )
    ):
        __slots__ = ()

        @property
        def screen_rect(self):
            return Rect.of(self.window.size, self.screen_pos)

    _SHADOW_OFFSET = Pos(16, 16)

    def __init__(self, screen, palette, toolkit, main_handler, fps_limit=20):
        self.screen = screen
        self.palette = palette
        self.toolkit = toolkit
        self.fps_limit = fps_limit

        self.buffer_surface = pygame.Surface(
            (screen.get_width(), screen.get_height()),
            depth=8,
        )
        self.buffer_surface.set_palette(toolkit.get_palette())

        self.buffer_image = Image(self.buffer_surface)

        self.running = False
        self.last_exception = None

        self.window_slots = []
        self.state = {}         # defaultdefaultdict()

        self.show_fps = False
        self._bg_fps = None

        self.show(main_handler, Pos(0, 0), 'main_handler')

    def show(self, window, screen_pos, state_key, casts_shadow=True):
        if state_key in self.state:
            raise Exception(f"Window for {state_key} is already shown!")

        self.state.update({state_key: window.initial_state_map})
        # print(yaml.dump(asdict(self.state)))

        if self.window_slots:
            bg_capture = self._capture_background(window, screen_pos, casts_shadow)
            if bg_capture.size.w > window.size.w or \
               bg_capture.size.h > window.size.h:
                self._cast_shadow(bg_capture, Rect.of(window.size, screen_pos))

        else:
            bg_capture = None

        self.window_slots.append(
            WindowManager.WindowSlot(window, screen_pos, state_key, bg_capture)
        )

        window.dirty()          # FIXME: redundant?

    def close(self, return_key):
        slot = self.window_slots.pop()
        if slot.bg_capture:
            with self.buffer_image.get_context() as ctx:
                slot.bg_capture.render(ctx, slot.screen_pos)

        if return_key:
            return_value = slot.window.make_return_value(self.state[slot.state_key])

        else:
            return_value = None

        fhomm.event.post_window_close(slot.state_key, return_key, return_value)

    def _capture_background(self, window, screen_pos, casts_shadow):
        if casts_shadow and (
                window.size.w < self.screen.get_width() or
                window.size.h < self.screen.get_height()
        ):
            capture_size = Size(
                window.size.w + WindowManager._SHADOW_OFFSET.x,
                window.size.h + WindowManager._SHADOW_OFFSET.y,
            )

        else:
            capture_size = window.size

        with self.buffer_image.get_context() as ctx:
            return ctx.capture(Rect.of(capture_size, screen_pos))

    def _cast_shadow(self, background, screen_rect):
        img_shadow = fhomm.render.Context.make_shadow_image(screen_rect.size)

        with self.buffer_image.get_context() as ctx:
            bg_copy = ctx.copy_image_for_shadow(background)
            img_shadow.render(bg_copy.get_context(), WindowManager._SHADOW_OFFSET)
            bg_copy.render(ctx, screen_rect.pos)

    def active_slot(self):
        return self.window_slots[-1]

    def render_active_window(self, force=True): # False
        slot = self.active_slot()

        with self.buffer_image.get_context().restrict(slot.screen_rect) as ctx:
            return slot.window.render(ctx, self.state[slot.state_key], force)

    def render_fps(self, ctx, dt):
        fps = 0 if dt == 0 else 1000 / dt
        fps_text = "%.1f" % fps

        font = self.toolkit.get_font()
        layout = font.layout_text(fps_text)
        size = font.measure_layout(layout)
        pos = Pos(0, 0)

        if self._bg_fps is not None:
            self._bg_fps.render(ctx, pos)

        self._bg_fps = ctx.capture(Rect.of(size, pos))

        font.draw_layout(ctx, layout, pos)

    def handle_global(self, event):
        # kind of has to be here to always react
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_F1:
                return fhomm.command.CMD_TOGGLE_DEBUG_UI_RENDER

            elif event.key == pygame.K_F2:
                return fhomm.command.CMD_TOGGLE_DEBUG_UI_EVENTS

            elif event.key == pygame.K_F3:
                return fhomm.command.CMD_TOGGLE_FPS

            elif event.key == pygame.K_F4:
                return fhomm.command.CMD_TOGGLE_FULLSCREEN

            elif event.key == pygame.K_q and event.mod & pygame.KMOD_CTRL:
                return fhomm.command.CMD_QUIT # DEBUG: fast quit

        elif event.type == fhomm.event.EVENT_WINDOW_CLOSED:
            return fhomm.command.cmd_clear_state(event.state_key)

    def handle_by_active_window(self, event):
        slot = self.active_slot()
        return slot.window.handle(
            self.state[slot.state_key],
            fhomm.ui.Window.translate_event(event, slot.screen_pos),
        )

    def handle_event(self, event):
        return fhomm.command.aslist(self.handle_global(event)) + \
            fhomm.command.aslist(self.handle_by_active_window(event))

    # def on_event(self, state, event):
    #     if event.type == pygame.QUIT:
    #         return fhomm.command.CMD_QUIT

    # TODO: this can be separated to a MainLoop or something
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
                slot = self.active_slot()
                cmds = self.handle_event(event)
                for cmd in cmds:
                    self.run_command(slot, cmd)

            if self.render_active_window():
                self.flush_buffer()

            self.tick_clock()

    def flush_buffer(self):
        with fhomm.render.Context(self.screen) as screen_ctx:
            self.buffer_image.render(screen_ctx)

        pygame.display.flip()

    def tick_clock(self):
        dt = self.clock.tick(self.fps_limit)

        if self.show_fps:
            with self.buffer_image.get_context() as ctx:
                self.render_fps(ctx, dt)

        # TODO: move to handle_global
        if self.palette.update_tick(dt):
            self.buffer_surface.set_palette(self.palette.palette)

        fhomm.event.post_tick(dt)

    @contextmanager
    def logging_just_once(self):
        try:
            yield
            self.last_exception = None
        except Exception as e:
            if self.last_exception is None:
                traceback.print_exc()

            self.last_exception = e

    def run_command(self, slot, command):
        if fhomm.ui.DEBUG_EVENTS:
            print(command)

        # TODO: table-based dispatch
        if command.code == fhomm.command.QUIT:
            self.running = False

        elif command.code == fhomm.command.IGNORE:
            pass

        elif command.code == fhomm.command.TOGGLE_DEBUG_UI_RENDER:
            fhomm.ui.DEBUG_RENDER = not fhomm.ui.DEBUG_RENDER
            slot.window.dirty()

        elif command.code == fhomm.command.TOGGLE_DEBUG_UI_EVENTS:
            fhomm.ui.DEBUG_EVENTS = not fhomm.ui.DEBUG_EVENTS

        elif command.code == fhomm.command.TOGGLE_FPS:
            self.show_fps = not self.show_fps

        elif command.code == fhomm.command.TOGGLE_FULLSCREEN:
            pygame.display.toggle_fullscreen()

        elif command.code == fhomm.command.SHOW:
            self.show(**command.kwargs)

        elif command.code == fhomm.command.CLOSE:
            self.close(**command.kwargs)

        elif command.code == fhomm.command.CLEAR_STATE:
            self.clear_state(**command.kwargs)

        elif command.code == fhomm.command.UPDATE:
            self.update_state(slot, **command.kwargs)

        else:
            print(f"unknown command: {command}")

    def update_state(self, slot, key, update_fn):
        # print(f"update_state: {key} {update_fn}")
        active_state = self.state[slot.state_key]
        old = active_state[key]
        new = update_fn(old)
        if old != new:
            # TODO: here we know we need to re-render, but otherwise not really
            active_state.update({key: new})
            fhomm.event.post_state_update(key, old, new)

    def clear_state(self, state_key):
        if state_key not in self.state:
            raise Exception(f"Window for {state_key} was not shown!")

        del self.state[state_key]
