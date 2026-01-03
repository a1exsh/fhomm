import pygame

from fhomm.render import Size
from fhomm.window.select import ItemSelectorWindow
import fhomm.game.monsters
import fhomm.ui


class ArmySelectorWindow(ItemSelectorWindow):
    def __init__(self, toolkit):
        items = [
            fhomm.ui.ImgList.Item(
                toolkit.load_sprite('mons32.icn', i),
                monster.name,
            )
            for i, monster in enumerate(fhomm.game.monsters.MONSTERS)
        ]
        super().__init__(toolkit, "Select Army:", items, Size(32, 32))
