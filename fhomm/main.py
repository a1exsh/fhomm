import os
import sys
import threading

import pygame

from fhomm.ui.screen.title_screen import TitleScreen
from fhomm.ui.window_manager import WindowManager
import fhomm.resource.agg
import fhomm.resource.loader
import fhomm.toolkit
import fhomm.ui.palette


HEROES_AGG_PATH = os.path.join(os.getenv('FHOMM_DATA'), 'HEROES.AGG')
HEROES_AGG = fhomm.resource.agg.open_file(HEROES_AGG_PATH)

RESOURCE_LOADER = fhomm.resource.loader.CachingLoader(
    fhomm.resource.loader.AggResourceLoader(HEROES_AGG),
)

TOOLKIT = fhomm.toolkit.Toolkit(RESOURCE_LOADER, 'kb.pal')
PALETTE = fhomm.ui.palette.Palette(TOOLKIT.get_palette())

# pygame setup
pygame.init()
SCREEN = pygame.display.set_mode((640, 480), depth=8)
SCREEN.set_palette(TOOLKIT.get_palette())

# DEBUG
# def render_palette(screen, size, offx, offy):
#     for y in range(16):
#         for x in range(16):
#             screen.fill((y << 4) | x, (offx + x*size, offy + y*size, size, size))

WINDOW_MANAGER = WindowManager(
    SCREEN,
    PALETTE,
    TOOLKIT,
    TitleScreen(TOOLKIT)
)
if sys.argv[-1] == '--background':
    threading.Thread(target=WINDOW_MANAGER).start()
else:
    WINDOW_MANAGER.run_event_loop()
