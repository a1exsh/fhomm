from fhomm.render import Pos
import fhomm.handler
import fhomm.window.main_menu
import fhomm.ui


class TitleScreen(fhomm.ui.Element): # Screen
    def __init__(self, loader):
        super().__init__()
        self.loader = loader
        self.bg_image = self.loader.load_image('heroes.bmp')
        self.measure(self.bg_image.size)

        self.main_menu = None

    def on_tick(self, dt):
        if self.main_menu is None:
            self.main_menu = fhomm.window.main_menu.Handler(self.loader)
            return fhomm.handler.cmd_show(self.main_menu, Pos(401, 35))

    def on_render(self, ctx):
        self.bg_image.render(ctx)
