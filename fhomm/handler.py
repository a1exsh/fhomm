from collections import namedtuple

import pygame

# EVENT_INIT = pygame.USEREVENT   # pygame.event.custom_type()
EVENT_TICK = pygame.USEREVENT + 1

QUIT = -1
IGNORE = 0
TOGGLE_FULLSCREEN = 1
SHOW = 2                        # open a new window or a screen
CLOSE = 3                       # close the active window or a screen
TOGGLE_DEBUG_UI = 4
# COMPOSE = ...              # could be expressed by posting events to the queue

Command = namedtuple('Command', ['code', 'kwargs'], defaults=[{}])

CMD_QUIT = Command(QUIT)
CMD_IGNORE = Command(IGNORE)
CMD_TOGGLE_FULLSCREEN = Command(TOGGLE_FULLSCREEN)
CMD_CLOSE = Command(CLOSE)
CMD_TOGGLE_DEBUG_UI = Command(TOGGLE_DEBUG_UI)


def cmd_show(element, screen_pos):
    return Command(
        SHOW,
        {
            'element': element,
            'screen_pos': screen_pos,
        }
    )
