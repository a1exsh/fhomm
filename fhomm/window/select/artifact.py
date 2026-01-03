import pygame

from fhomm.window.select import ItemSelectorWindow
import fhomm.game.artifacts
import fhomm.ui.list


class ArtifactSelectorWindow(ItemSelectorWindow):
    def __init__(self, loader):
        items = [
            fhomm.ui.list.Item(
                loader.load_sprite('artfx.icn', i),
                artifact.name,
            )
            for i, artifact in enumerate(fhomm.game.artifacts.ARTIFACTS)
        ]
        super().__init__(loader, "Select Artifact:", items, items[0].img.size)
