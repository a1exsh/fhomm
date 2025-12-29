import os
import sys
import threading
import pygame

import fhomm.agg
import fhomm.pal
import fhomm.bmp
import fhomm.icn
import fhomm.loader
import fhomm.palette
import fhomm.render
from fhomm.render import Pos, Rect
import fhomm.ui
import fhomm.handler
import fhomm.main_menu


# class Image(object):
#     def __init__(self, img):
#         self.img = img

#     def render(self, screen, pos):
#         screen.blit(self.img, pos)

#     def get_width(self):
#         return self.img.get_width()

#     def get_height(self):
#         return self.img.get_height()


# class Sprite(Image):
#     def __init__(self, img, offx, offy):
#         super().__init__(img)
#         self.offx = offx
#         self.offy = offy

#     def render(self, screen, pos):
#         screen.blit(self.img, (pos.x + self.offx, pos.y + self.offy))


class PygameLoader(object):
    def __init__(self, loader, palette):
        self.loader = loader
        self.palette = palette

    def load_image(self, bmp_name):
        bmp = self.loader.load_bmp(bmp_name)
        img = self.make_image(bmp.data, bmp.width, bmp.height)
        return fhomm.render.Image(img)

    def load_sprite(self, icn_name, idx):
        s = self.loader.load_icn(icn_name)[idx]
        img = self.make_image(s.data, s.width, s.height)
        img.set_colorkey(0)
        return fhomm.render.Sprite(img, Pos(s.offx, s.offy))

    def make_image(self, data, width, height):
        img = pygame.image.frombuffer(data, (width, height), 'P')
        img.set_palette(self.palette)
        return img


def pal_to_pygame(palette):
    return [
        (
            4*palette[i*3],
            4*palette[i*3+1],
            4*palette[i*3+2],
        )
        for i in range(256)
    ]


HEROES_AGG_PATH = os.path.join(os.getenv('FHOMM_DATA'), 'HEROES.AGG')
AGG = fhomm.agg.open_file(HEROES_AGG_PATH)

PYGAME_PALETTE = pal_to_pygame(fhomm.pal.read_palette(AGG))
PALETTE = fhomm.palette.Palette(PYGAME_PALETTE)

PYGAME_LOADER = PygameLoader(
    fhomm.loader.CachingLoader(fhomm.loader.Loader(AGG)),
    PYGAME_PALETTE,
)

# pygame setup
pygame.init()
SCREEN = pygame.display.set_mode((640, 480), depth=8)
SCREEN.set_palette(PALETTE.palette)

FONT = pygame.font.SysFont('Mono', 16)
FPS_COLOR = pygame.color.Color('white')

# DRAGON = load_icn(AGG, 'dragon.wlk')
# PHOENIX = load_icn(AGG, 'phoenix.wlk')

# DRAGFLY = [sprite_to_sdl(sprite) for sprite in DRAGON[0:6]]
# PHOEFLY = [sprite_to_sdl(sprite) for sprite in PHOENIX[0:6]]


def render(screen):
    #screen.blit(DRAGFLY[1], (250, 100))
    screen.blit(PHOEFLY[0], (250, 150))


# DEBUG
def render_fps(screen, dt):
    fps = 0 if dt == 0 else 1000 // dt
    s = FONT.render(str(fps), False, FPS_COLOR)
    screen.blit(s, (0,0))       # screen.get_width() - s.get_width()


def render_palette(screen, size, offx, offy):
    for y in range(16):
        for x in range(16):
            screen.fill((y << 4) | x, (offx + x*size, offy + y*size, size, size))


class MainHandler(fhomm.ui.Element):
    def __init__(self, loader):
        super().__init__(loader)
        self.bg_image = self.loader.load_image('heroes.bmp')
        self.measure(self.bg_image.dim)

        self.attach(
            fhomm.main_menu.Handler(self.loader),
            Pos(401, 35),
        )

    def on_event(self, event):
        # cmd = super().on_event(event)
        # if cmd is not None:
        #     return cmd

        if event.type == pygame.QUIT:
            return fhomm.handler.CMD_QUIT

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F4:
                return fhomm.handler.CMD_TOGGLE_FULLSCREEN

    def on_render(self, ctx):
        self.bg_image.render(ctx)


class Game(object):
    def __init__(self, loader, screen):
        self.loader = loader
        self.handler = MainHandler(loader)
        self.screen = screen

    def __call__(self):
        self.run()

    def run(self):
        clock = pygame.time.Clock()

        # render_palette(SCREEN, 8, 258, 8)
        # render_fps(SCREEN, PALETTE_CYCLE_TICK)
        screen_ctx = fhomm.render.Context(self.screen)

        self.running = True
        while self.running:
            for event in pygame.event.get():
                command = self.handler.handle(event)
                if command is not None:
                    self.run_command(command)

            if self.handler.render(screen_ctx):
                # print("flippin")
                pygame.display.flip()

            dt = clock.tick(60)
            if PALETTE.update_tick(dt):
                SCREEN.set_palette(PALETTE.palette)

        pygame.quit()

    def run_command(self, command):
        if command.code == fhomm.handler.QUIT:
            self.running = False

        elif command.code == fhomm.handler.TOGGLE_FULLSCREEN:
            pygame.display.toggle_fullscreen()

        # elif command.code == fhomm.handler.COMPOSE:
        #     for cmd in command.kwargs['commands']:
        #         self.run_command(cmd, handler)

        else:
            print(f"unknown command from handler: {command}")


game = Game(PYGAME_LOADER, SCREEN)
threading.Thread(target=game).start()
