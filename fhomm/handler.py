from collections import namedtuple

import pygame

# EVENT_INIT = pygame.USEREVENT   # pygame.event.custom_type()
EVENT_TICK = pygame.USEREVENT + 1

QUIT = -1
# RENDER = 0
PUSH_HANDLER = 1
# COMPOSE = 2
TOGGLE_FULLSCREEN = 3

Command = namedtuple('Command', ['code', 'kwargs'], defaults=[{}])

CMD_QUIT = Command(QUIT)
# CMD_RENDER = Command(RENDER)
CMD_TOGGLE_FULLSCREEN = Command(TOGGLE_FULLSCREEN)


def cmd_push_handler(handler, screen_pos):
    return Command(
        PUSH_HANDLER,
        {
            'handler': handler,
            'screen_pos': screen_pos,
        }
    )


# def cmd_compose(*cmds):
#     return Command(COMPOSE, {'commands': cmds})
