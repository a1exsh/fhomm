import pygame

from fhomm.render import Pos
from fhomm.window.select import ItemSelectorWindow
import fhomm.game.heroes
import fhomm.handler
import fhomm.ui.list


class HeroSelectorWindow(ItemSelectorWindow):
    def __init__(self, toolkit, title, return_key):
        items = [
            fhomm.ui.list.Item(
                HeroSelectorWindow.make_portrait_with_bg(toolkit, i),
                hero.name,
            )
            for i, hero in enumerate(fhomm.game.heroes.HEROES)
        ]
        super().__init__(
            toolkit,
            title,
            items,
            items[0].img.size,
            return_key,
        )

    @staticmethod
    def make_portrait_with_bg(toolkit, idx):
        res = toolkit.load_sprite('locators.icn', 21).make_copy()
        with res.get_context() as ctx:
            toolkit.load_sprite('miniport.icn', idx).render(ctx, Pos(4, 4))
            return res
