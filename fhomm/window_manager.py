import pygame

from fhomm.render import Pos, Dim, Rect
import fhomm.handler
import fhomm.ui


class WindowManager(fhomm.ui.Container):

    def __init__(self, screen, palette, main_handler):
        super().__init__()
        self.screen = screen
        self.palette = palette

        self.screen_ctx = fhomm.render.Context(screen)
        self.captured_background = []
        self.running = False

        self.measure(Dim(screen.get_width(), screen.get_height()))

        self.show(main_handler, Pos(0, 0))

    def attach(self, element, pos):
        raise Exception("Elements should not be attached to window manager directly!")

    def detach(self, element):
        raise Exception("Elements should not be detached from window manager directly!")

    def show(self, element, screen_pos):
        super().attach(element, screen_pos)

        bg_rect = Rect(element.dim, screen_pos)
        self.captured_background.append(self.screen_ctx.capture(bg_rect))

        element.dirty()

    def close_active(self):
        child = self.active_child()
        super().detach(child.element)

        print(f"remaining slots: {self.child_slots}")

        self.captured_background.pop().render(self.screen_ctx, child.relpos)

    def active_child(self):
        return self.child_slots[-1]

    def render(self, ctx, force=False):
        return self.render_child(self.active_child(), ctx, force)

    def handle(self, event):
        # kind of has to be here to always react
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_F4:
                return fhomm.handler.CMD_TOGGLE_FULLSCREEN

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

        self.running = True
        while self.running:
            for event in pygame.event.get():
                command = self.handle(event)
                if command is not None:
                    self.run_command(command)

            if self.render(self.screen_ctx):
                # print("flippin")
                pygame.display.flip()

            dt = clock.tick(60)

            # TODO: for now no way to move it to on_event, as a child handling
            # on tick will prevent palette from cycling a way to solve it may
            # be by re-thinking the short-circuit on first returned command
            if self.palette.update_tick(dt):
                self.screen.set_palette(self.palette.palette)

            self.post_tick(dt)

        pygame.quit()

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

        elif command.code == fhomm.handler.SHOW:
            self.show(**command.kwargs)

        elif command.code == fhomm.handler.CLOSE:
            self.close_active()

        # elif command.code == fhomm.handler.COMPOSE:
        #     for cmd in command.kwargs['commands']:
        #         self.run_command(cmd, handler)

        else:
            print(f"unknown command: {command}")
