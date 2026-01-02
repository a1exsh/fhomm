import pygame

import fhomm.game.heroes
import fhomm.handler
import fhomm.ui
import fhomm.window.selector


class Handler(fhomm.window.selector.Handler):
    def __init__(self, loader, title):
        items = [
            fhomm.ui.ImgList.Item(
                loader.load_sprite('miniport.icn', i),
                hero.name,
            )
            for i, hero in enumerate(fhomm.game.heroes.HEROES)
        ]
        # loader.load_sprite('locators.icn', 21),
        super().__init__(loader, title, items, items[0].img.size)
