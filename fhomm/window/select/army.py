import pygame

from fhomm.render import Pos, Size, Rect
from fhomm.window.select import ItemSelectorWindow
import fhomm.game.monsters
import fhomm.ui.list


class ArmySelectorWindow(ItemSelectorWindow):
    def __init__(self, toolkit, return_key):
        items = [
            fhomm.ui.list.Item(
                ArmySelectorWindow.make_minimon_with_swapbg(toolkit, i),
                monster.name,
            )
            for i, monster in enumerate(fhomm.game.monsters.MONSTERS)
        ]
        super().__init__(
            toolkit,
            "Select Army:",
            items,
            Size(34, 34),
            return_key,
        )

    @staticmethod
    def make_minimon_with_swapbg(toolkit, idx):
        with toolkit.load_image('swapwin.bmp').get_context() as bg_ctx:
            res = bg_ctx.capture(Rect(23, 147, 34, 34))
            with res.get_context() as ctx:
                toolkit.load_sprite('mons32.icn', idx).render(ctx, Pos(1, 1))
                return res
