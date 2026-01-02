import os
import sys
import threading

import pygame

import fhomm.resource.agg
import fhomm.resource.loader
import fhomm.palette
from fhomm.pygame_loader import PygameLoader
from fhomm.window_manager import WindowManager
from fhomm.window.title_screen import TitleScreen


HEROES_AGG_PATH = os.path.join(os.getenv('FHOMM_DATA'), 'HEROES.AGG')
HEROES_AGG = fhomm.resource.agg.open_file(HEROES_AGG_PATH)

PYGAME_LOADER = PygameLoader(
    fhomm.resource.loader.CachingLoader(
        fhomm.resource.loader.AggResourceLoader(HEROES_AGG),
    ),
    'kb.pal',
)
PALETTE = fhomm.palette.Palette(PYGAME_LOADER.palette)

# pygame setup
pygame.init()
SCREEN = pygame.display.set_mode((640, 480), depth=8)
SCREEN.set_palette(PYGAME_LOADER.palette)

FONT = PYGAME_LOADER.get_font()

# DEBUG
# def render_palette(screen, size, offx, offy):
#     for y in range(16):
#         for x in range(16):
#             screen.fill((y << 4) | x, (offx + x*size, offy + y*size, size, size))

window_manager = WindowManager(
    SCREEN,
    PALETTE,
    FONT,
    TitleScreen(PYGAME_LOADER)
)
threading.Thread(target=window_manager).start()
