QUIT = -1
RENDER = 0


class Handler(object):
    def __init__(self, screen, loader, handlers):
        self.screen = screen
        self.loader = loader
        self.handlers = handlers
        self.first_run = True
