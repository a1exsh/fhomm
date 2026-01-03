from fhomm.render import Pos
from fhomm.window.menu.main import MainMenu
import fhomm.handler
import fhomm.ui


class TitleScreen(fhomm.ui.Element): # Screen
    def __init__(self, toolkit):
        super().__init__()
        self.toolkit = toolkit
        self.bg_image = toolkit.load_image('heroes.bmp')
        self.measure(self.bg_image.size)

        self.main_menu = None

    def on_tick(self, dt):
        if self.main_menu is None:
            self.main_menu = MainMenu(self.toolkit)
            return fhomm.handler.cmd_show(self.main_menu, Pos(401, 35))

    def on_render(self, ctx):
        self.bg_image.render(ctx)
