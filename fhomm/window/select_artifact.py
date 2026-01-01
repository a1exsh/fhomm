import pygame

import fhomm.ui
import fhomm.handler
import fhomm.window.selector
from fhomm.render import Pos, Dim


class Handler(fhomm.window.selector.Handler):
    def __init__(self, loader):
        items = [
            fhomm.ui.ImgList.Item(
                loader.load_sprite('artfx.icn', i),
                "%02d".format(i),
            )
            for i in range(38)
        ]
        super().__init__(loader, items, items[0].img.dim)
