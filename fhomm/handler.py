from collections import namedtuple

import pygame

# EVENT_INIT = pygame.USEREVENT   # pygame.event.custom_type()

QUIT = -1
# RENDER = 0
# PUSH_HANDLER = 1
# COMPOSE = 2

Command = namedtuple('Command', ['code', 'kwargs'], defaults=[None])

CMD_QUIT = Command(QUIT)
# CMD_RENDER = Command(RENDER)


# def cmd_push_handler(handler):
#     return Command(PUSH_HANDLER, {'handler': handler})


# def cmd_compose(*cmds):
#     return Command(COMPOSE, {'commands': cmds})
