import os
import sys
import threading
import pygame

import fhomm.agg
import fhomm.bmp
import fhomm.pal

FPS_COLOR = pygame.color.Color('white')


def pal_to_sdl(palette):
    return [
        (
            4*palette[i*3],
            4*palette[i*3+1],
            4*palette[i*3+2],
        )
        for i in range(256)
    ]


def bmp_to_sdl(bmp):
    s = pygame.image.frombuffer(bmp.data, (bmp.width, bmp.height), 'P')
    s.set_palette(SDL_PALETTE)
    return s


def load_bmp(agg, name):
    agg.f.seek(agg.entries[name].offset, os.SEEK_SET)
    return fhomm.bmp.read_bitmap(agg.f)


pygame.init()
SCREEN = pygame.display.set_mode((640, 480))

FONT = pygame.font.SysFont('Mono', 16)

HEROES_AGG_PATH = os.path.join(os.getenv('FHOMM_DATA'), 'HEROES.AGG')
AGG = fhomm.agg.open_file(HEROES_AGG_PATH)

PALETTE = fhomm.pal.read_palette(AGG.f, AGG.entries)


SDL_PALETTE = pal_to_sdl(PALETTE)
HEROESBG = bmp_to_sdl(load_bmp(AGG, 'heroes.bmp'))
REDBACK = bmp_to_sdl(load_bmp(AGG, 'redback.bmp'))


def render(screen):
    screen.blit(HEROESBG, (0, 0))
    screen.blit(REDBACK, (screen.get_width() - (REDBACK.get_width() + 46), 35))


def render_fps(screen, dt):
    fps = 0 if dt == 0 else 1000 // dt
    s = FONT.render(str(fps), False, FPS_COLOR)
    screen.blit(s, (0,0))       # screen.get_width() - s.get_width()


def game_loop():
    clock = pygame.time.Clock()
    running = True
    dt = 0

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        render(SCREEN)
        render_fps(SCREEN, dt)

        # flip() the display to put your work on screen
        pygame.display.flip()

        dt = clock.tick(60)  # limits FPS to 60

    pygame.quit()


threading.Thread(target=game_loop).start()
