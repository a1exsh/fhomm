import os
import sys
import threading
import pygame

import fhomm.agg
import fhomm.pal
import fhomm.bmp
import fhomm.icn
import fhomm.palette


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


def sprite_to_sdl(sprite):
    s = pygame.image.frombuffer(sprite.data, (sprite.width, sprite.height), 'P')
    s.set_colorkey(0)
    s.set_palette(SDL_PALETTE)
    return s


def load_bmp(agg, name):
    agg.f.seek(agg.entries[name].offset, os.SEEK_SET)
    return fhomm.bmp.read_bitmap(agg.f)


def load_icn(agg, name):
    agg.f.seek(agg.entries[name].offset, os.SEEK_SET)
    return fhomm.icn.read_icn_sprites(agg.f)


HEROES_AGG_PATH = os.path.join(os.getenv('FHOMM_DATA'), 'HEROES.AGG')
AGG = fhomm.agg.open_file(HEROES_AGG_PATH)

SDL_PALETTE = pal_to_sdl(fhomm.pal.read_palette(AGG))
PALETTE = fhomm.palette.Palette(SDL_PALETTE)

# pygame setup
pygame.init()
SCREEN = pygame.display.set_mode((640, 480), depth=8)
SCREEN.set_palette(PALETTE.palette)

FONT = pygame.font.SysFont('Mono', 16)
FPS_COLOR = pygame.color.Color('white')


HEROESBG = bmp_to_sdl(load_bmp(AGG, 'heroes.bmp'))
REDBACK = bmp_to_sdl(load_bmp(AGG, 'redback.bmp'))

BTNMAIN = load_icn(AGG, 'btnmain.icn')
BTNLOAD = sprite_to_sdl(BTNMAIN[0])
BTNNEW = sprite_to_sdl(BTNMAIN[2])
BTNSCORE = sprite_to_sdl(BTNMAIN[4])
BTNCREDITS = sprite_to_sdl(BTNMAIN[6])
BTNQUIT = sprite_to_sdl(BTNMAIN[8])

DRAGON = load_icn(AGG, 'dragon.wlk')
PHOENIX = load_icn(AGG, 'phoenix.wlk')

DRAGFLY = [sprite_to_sdl(sprite) for sprite in DRAGON[0:6]]
PHOEFLY = [sprite_to_sdl(sprite) for sprite in PHOENIX[0:6]]


def render(screen):
    screen.blit(HEROESBG, (0, 0))

    menu_pos = (screen.get_width() - (REDBACK.get_width() + 46), 35)
    screen.blit(REDBACK, menu_pos)
    screen.blit(BTNNEW,     (menu_pos[0] + 33, menu_pos[1] + 45))
    screen.blit(BTNLOAD,    (menu_pos[0] + 33, menu_pos[1] + 45 + 66))
    screen.blit(BTNSCORE,   (menu_pos[0] + 33, menu_pos[1] + 45 + 66*2))
    screen.blit(BTNCREDITS, (menu_pos[0] + 33, menu_pos[1] + 45 + 66*3))
    screen.blit(BTNQUIT,    (menu_pos[0] + 33, menu_pos[1] + 45 + 66*4))

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


def game_loop_step():
    pass


def game_loop():
    clock = pygame.time.Clock()

    render(SCREEN)
    # render_palette(SCREEN, 8, 258, 8)
    # render_fps(SCREEN, PALETTE_CYCLE_TICK)
    pygame.display.flip()

    running = True
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        dt = clock.tick(60)
        if PALETTE.update_tick(dt):
            SCREEN.set_palette(PALETTE.palette)

        game_loop_step()

    pygame.quit()


threading.Thread(target=game_loop).start()
