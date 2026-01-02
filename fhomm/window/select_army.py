import pygame

from fhomm.render import Size
import fhomm.game.monsters
import fhomm.handler
import fhomm.ui
import fhomm.window.selector


class Handler(fhomm.window.selector.Handler):
    def __init__(self, loader):
        items = [
            fhomm.ui.ImgList.Item(
                loader.load_sprite('mons32.icn', i),
                monster.name,
            )
            for i, monster in enumerate(fhomm.game.monsters.MONSTERS)
        ]
        super().__init__(loader, "Select Army:", items, Size(32, 32))
