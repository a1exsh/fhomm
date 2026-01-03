from fhomm.render import Pos
from fhomm.window.menu.main import MainMenu
import fhomm.handler
import fhomm.ui


class TitleScreen(fhomm.ui.Element): # screen, not a window
    def __init__(self, toolkit):
        self.toolkit = toolkit
        self.image = toolkit.load_image('heroes.bmp')
        super().__init__(self.image.size)

        self.main_menu = None

    def on_tick(self, dt):
        if self.main_menu is None:
            self.main_menu = MainMenu(self.toolkit)
            return fhomm.handler.cmd_show(self.main_menu, Pos(401, 35))

    def on_render(self, ctx):
        self.image.render(ctx)
