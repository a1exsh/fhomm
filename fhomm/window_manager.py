from contextlib import contextmanager
import traceback

import pygame

from fhomm.render import Pos, Size, Rect
import fhomm.handler
import fhomm.ui


class WindowManager(fhomm.ui.Container):

    _SHADOW_OFFSET = Pos(16, 16)

    def __init__(self, screen, palette, main_handler, fps_limit=30):
        super().__init__()
        self.screen = screen
        self.palette = palette
        self.fps_limit = fps_limit

        self.screen_ctx = fhomm.render.Context(screen)
        self.bg_captures = []
        self.running = False

        self.measure(Size(screen.get_width(), screen.get_height()))

        self.show(main_handler, Pos(0, 0))

    def attach(self, element, pos):
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
            bg_rect = Rect(capture_size, screen_pos)
        else:
            shadow = False
            bg_rect = Rect(element.size, screen_pos)

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

    def render(self, ctx, force=False):
        return self.render_child(self.active_child(), ctx, force)

    def handle(self, event):
        # kind of has to be here to always react
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_F4:
                return fhomm.handler.CMD_TOGGLE_FULLSCREEN

            elif event.key == pygame.K_F1:
                return fhomm.handler.CMD_TOGGLE_DEBUG_UI_RENDER

            elif event.key == pygame.K_F2:
                return fhomm.handler.CMD_TOGGLE_DEBUG_UI_EVENTS

        cmd = self.handle_by_child(self.active_child(), event)
        if cmd is not None:
            return cmd

        return self.on_event(event)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            return fhomm.handler.CMD_QUIT

    def __call__(self):
        self.run_event_loop()

    def run_event_loop(self):
        clock = pygame.time.Clock()

        # render_palette(SCREEN, 8, 258, 8)
        # render_fps(SCREEN, PALETTE_CYCLE_TICK)

        self.last_exception = None

        self.running = True
        while self.running:
            with self.logging_just_once():
                for event in pygame.event.get():
                    command = self.handle(event)
                    if command is not None:
                        self.run_command(command)

                if self.render(self.screen_ctx):
                    # print("flippin")
                    pygame.display.flip()

                dt = clock.tick(self.fps_limit)

                # TODO: for now no way to move it to on_event, as a child
                # handling on tick will prevent palette from cycling a way to
                # solve it may be by re-thinking the short-circuit on first
                # returned command
                if self.palette.update_tick(dt):
                    self.screen.set_palette(self.palette.palette)

                self.post_tick(dt)

        pygame.quit()

    @contextmanager
    def logging_just_once(self):
        try:
            yield
            self.last_exception = None
        except Exception as e:
            if self.last_exception is None:
                traceback.print_exc()

            self.last_exception = e

    def post_tick(self, dt):
        pygame.event.post(pygame.event.Event(fhomm.handler.EVENT_TICK, dt=dt))

    def run_command(self, command):
        # TODO: table-based dispatch
        if command.code == fhomm.handler.QUIT:
            self.running = False

        elif command.code == fhomm.handler.IGNORE:
            pass

        elif command.code == fhomm.handler.TOGGLE_FULLSCREEN:
            pygame.display.toggle_fullscreen()

        elif command.code == fhomm.handler.TOGGLE_DEBUG_UI_RENDER:
            fhomm.ui.DEBUG_RENDER = not fhomm.ui.DEBUG_RENDER
            self.active_child().element.dirty()

        elif command.code == fhomm.handler.TOGGLE_DEBUG_UI_EVENTS:
            fhomm.ui.DEBUG_EVENTS = not fhomm.ui.DEBUG_EVENTS

        elif command.code == fhomm.handler.SHOW:
            self.show(**command.kwargs)

        elif command.code == fhomm.handler.CLOSE:
            self.close_active()

        # elif command.code == fhomm.handler.COMPOSE:
        #     for cmd in command.kwargs['commands']:
        #         self.run_command(cmd, handler)

        else:
            print(f"unknown command: {command}")
