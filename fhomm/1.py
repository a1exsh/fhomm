import os
import sys
import threading
import pygame

import fhomm.agg
import fhomm.pal
import fhomm.bmp
import fhomm.icn

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


def pal_cycle_index(i):
    if i < 224:
        return i
    elif i < 228:
        return 224 + ((i - 224) + 1) % 4
    elif i < 232:
        return 228 + ((i - 228) + 1) % 4
    elif i < 240:
        return i
    elif i < 245:
        return 240 + ((i - 240) + 1) % 5
    elif i < 251:
        return 245 + ((i - 245) + 1) % 6
    else:
        return i


def pal_cycle(palette):
    return [
        palette[pal_cycle_index(i)]
        for i in range(len(palette))
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

PALETTE = fhomm.pal.read_palette(AGG.f, AGG.entries)
SDL_PALETTE = pal_to_sdl(PALETTE)

# pygame setup
pygame.init()
SCREEN = pygame.display.set_mode((640, 480), depth=8)
SCREEN.set_palette(SDL_PALETTE)

FONT = pygame.font.SysFont('Mono', 16)


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


def render_fps(screen, dt):
    fps = 0 if dt == 0 else 1000 // dt
    s = FONT.render(str(fps), False, FPS_COLOR)
    screen.blit(s, (0,0))       # screen.get_width() - s.get_width()


PALETTE_CYCLE_TICK = 0
PAL_CYCLE_EVERY = 250

RENDERED_ONCE = False


def render_palette(screen, size, offx, offy):
    for y in range(16):
        for x in range(16):
            screen.fill((y << 4) | x, (offx + x*size, offy + y*size, size, size))


def game_loop_step(clock):
    global SDL_PALETTE
    global PALETTE_CYCLE_TICK
    global RENDERED_ONCE

    dt = clock.tick(10)  # limits FPS to 60

    if not RENDERED_ONCE:
        render(SCREEN)
        render_palette(SCREEN, 8, 258, 8)
        render_fps(SCREEN, PALETTE_CYCLE_TICK)

        pygame.display.flip()
        RENDERED_ONCE = True

    PALETTE_CYCLE_TICK += dt

    if PALETTE_CYCLE_TICK >= PAL_CYCLE_EVERY:
        while PALETTE_CYCLE_TICK >= PAL_CYCLE_EVERY:
            SDL_PALETTE = pal_cycle(SDL_PALETTE)
            PALETTE_CYCLE_TICK -= PAL_CYCLE_EVERY

        SCREEN.set_palette(SDL_PALETTE)


def game_loop():
    clock = pygame.time.Clock()

    running = True
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game_loop_step(clock)

    pygame.quit()


threading.Thread(target=game_loop).start()
