# TODO: rename this file to something like "command"

from collections import namedtuple

import pygame

# EVENT_INIT = pygame.USEREVENT   # pygame.event.custom_type()
EVENT_TICK = pygame.USEREVENT + 1

QUIT = -1
IGNORE = 0
TOGGLE_FULLSCREEN = 1
SHOW = 2                        # open a new window or a screen
CLOSE = 3                       # close the active window or a screen
TOGGLE_DEBUG_UI_RENDER = 4
TOGGLE_DEBUG_UI_EVENTS = 5
TOGGLE_FPS = 6
# COMPOSE = ...              # could be expressed by posting events to the queue

Command = namedtuple('Command', ['code', 'kwargs'], defaults=[{}])

CMD_QUIT = Command(QUIT)
CMD_IGNORE = Command(IGNORE)
CMD_TOGGLE_FULLSCREEN = Command(TOGGLE_FULLSCREEN)
CMD_CLOSE = Command(CLOSE)
CMD_TOGGLE_DEBUG_UI_RENDER = Command(TOGGLE_DEBUG_UI_RENDER)
CMD_TOGGLE_DEBUG_UI_EVENTS = Command(TOGGLE_DEBUG_UI_EVENTS)
CMD_TOGGLE_FPS = Command(TOGGLE_FPS)


def cmd_show(element, screen_pos):
    return Command(
        SHOW,
        {
            'element': element,
            'screen_pos': screen_pos,
        }
    )
