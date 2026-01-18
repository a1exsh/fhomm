from fhomm.render import Pos
from fhomm.window.menu.main import MainMenu
import fhomm.handler
import fhomm.ui


class TitleScreen(fhomm.ui.Window):
    def __init__(self, toolkit):
        super().__init__(toolkit.load_image('heroes.bmp'))
        self.toolkit = toolkit

        self.main_menu = None

        self.initial_state_map = {
            '_': {},
        }

    def on_tick(self, dt):
        if self.main_menu is None:
            self.main_menu = MainMenu(self.toolkit)
            return fhomm.handler.cmd_show(
                self.main_menu, Pos(401, 35), 'main_menu'
            )
