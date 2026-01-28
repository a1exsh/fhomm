import pygame

from fhomm.window.select import ItemSelectorWindow
import fhomm.game.artifacts
import fhomm.ui.list


class ArtifactSelectorWindow(ItemSelectorWindow):
    def __init__(self, toolkit, return_key):
        items = [
            fhomm.ui.list.Item(
                toolkit.load_sprite('artfx.icn', i),
                artifact.name,
            )
            for i, artifact in enumerate(fhomm.game.artifacts.ARTIFACTS)
        ]
        super().__init__(
            toolkit,
            "Select Artifact:",
            items,
            items[0].img.size,
            return_key,
        )
