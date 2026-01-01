import pygame

import fhomm.ui
import fhomm.handler
import fhomm.window.selector
from fhomm.render import Pos, Dim


class Handler(fhomm.window.selector.Handler):
    def __init__(self, loader):
        items = [
            fhomm.ui.ImgList.Item(
                loader.load_sprite('miniport.icn', i),
                "Miniport: %04d" % i,
            )
            for i in range(36)
        ]
        # loader.load_sprite('locators.icn', 21),
        super().__init__(loader, items, items[0].img.dim)
