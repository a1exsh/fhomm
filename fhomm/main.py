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
import fhomm.handler
import fhomm.main_menu


class PygameLoader(object):
    def __init__(self, loader, palette):
        self.loader = loader
        self.palette = palette

    def load_bmp(self, name):
        bmp = self.loader.load_bmp(name)
        s = pygame.image.frombuffer(bmp.data, (bmp.width, bmp.height), 'P')
        s.set_palette(self.palette)
        return s

    def load_sprite(self, name, idx):
        icn = self.loader.load_icn(name)
        sprite = icn[idx]
        s = pygame.image.frombuffer(sprite.data, (sprite.width, sprite.height), 'P')
        s.set_colorkey(0)
        s.set_palette(self.palette)
        return s


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


HEROESBG = PYGAME_LOADER.load_bmp('heroes.bmp')

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


class MainHandler(fhomm.handler.Handler):
    def run(self):
        if self.first_run:
            self.first_run = False
            self.handlers.append(
                fhomm.main_menu.Handler(self.screen, self.loader, self.handlers)
            )
            self.render()
            return fhomm.handler.RENDER

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return fhomm.handler.QUIT

    def render(self):
        self.screen.blit(self.loader.load_bmp('heroes.bmp'), (0, 0))


def game_loop():
    clock = pygame.time.Clock()

    handlers = []
    handlers.append(MainHandler(SCREEN, PYGAME_LOADER, handlers))

    # render_palette(SCREEN, 8, 258, 8)
    # render_fps(SCREEN, PALETTE_CYCLE_TICK)

    while True:
        handler = handlers[-1]
        cmd = handler.run()
        if cmd == fhomm.handler.QUIT:
            break
        elif cmd == fhomm.handler.RENDER:
            pygame.display.flip()

        dt = clock.tick(60)
        if PALETTE.update_tick(dt):
            SCREEN.set_palette(PALETTE.palette)

    pygame.quit()


threading.Thread(target=game_loop).start()
