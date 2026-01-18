# TODO: rename this file to something like "command"
from collections import namedtuple

import pygame

# EVENT_COMMAND = pygame.USEREVENT   # pygame.event.custom_type()
EVENT_TICK = pygame.USEREVENT + 1
EVENT_WINDOW_CLOSED = pygame.USEREVENT + 2


QUIT = -1
IGNORE = 0
TOGGLE_FULLSCREEN = 1
SHOW = 2                        # open a new window or a screen
CLOSE = 3                       # close the active window or a screen
TOGGLE_DEBUG_UI_RENDER = 4
TOGGLE_DEBUG_UI_EVENTS = 5
TOGGLE_FPS = 6
UPDATE = 7


Command = namedtuple('Command', ['code', 'kwargs'], defaults=[{}])

CMD_QUIT = Command(QUIT)
CMD_IGNORE = Command(IGNORE)
CMD_TOGGLE_FULLSCREEN = Command(TOGGLE_FULLSCREEN)
CMD_CLOSE = Command(CLOSE)
CMD_TOGGLE_DEBUG_UI_RENDER = Command(TOGGLE_DEBUG_UI_RENDER)
CMD_TOGGLE_DEBUG_UI_EVENTS = Command(TOGGLE_DEBUG_UI_EVENTS)
CMD_TOGGLE_FPS = Command(TOGGLE_FPS)


def cmd_show(window, screen_pos):
    return Command(
        SHOW,
        {
            'window': window,
            'screen_pos': screen_pos,
        }
    )


def cmd_update(update_fn):
    return Command(UPDATE, {'update_fn': update_fn})
