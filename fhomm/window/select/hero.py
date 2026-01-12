import pygame

from fhomm.window.select import ItemSelectorWindow
import fhomm.game.heroes
import fhomm.handler
import fhomm.ui.list


class HeroSelectorWindow(ItemSelectorWindow):
    def __init__(self, toolkit, title):
        items = [
            fhomm.ui.list.Item(
                toolkit.load_sprite('miniport.icn', i),
                hero.name,
            )
            for i, hero in enumerate(fhomm.game.heroes.HEROES)
        ]
        # toolkit.load_sprite('locators.icn', 21), # extra bg
        super().__init__(
            'select_hero',
            toolkit,
            title,
            items,
            items[0].img.size,
        )
