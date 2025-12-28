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


class Handler(object):
    def __init__(self, screen, loader):
        self.screen = screen
        self.loader = loader
        self.children = []
        self.needs_render = True

    def on_event(self, event):
        for child in self.children:
            cmd = child.on_event(event)
            if cmd is not None:
                return cmd

    def render(self):
        flip = False

        # self.needs_render = True
        if self.needs_render:
            # print(f"needs render: {self}")
            self.on_render()
            self.needs_render = False
            flip = True

        for child in self.children:
            if child.render():
                flip = True

        return flip
