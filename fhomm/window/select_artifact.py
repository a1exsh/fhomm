import pygame

import fhomm.game.artifacts
import fhomm.handler
import fhomm.ui
import fhomm.window.selector


class Handler(fhomm.window.selector.Handler):
    def __init__(self, loader):
        items = [
            fhomm.ui.ImgList.Item(
                loader.load_sprite('artfx.icn', i),
                artifact.name,
            )
            for i, artifact in enumerate(fhomm.game.artifacts.ARTIFACTS)
        ]
        super().__init__(loader, "Select Artifact:", items, items[0].img.size)
