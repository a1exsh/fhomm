import fhomm.render
from fhomm.toolkit.button_font import ButtonFont
import fhomm.ui
import fhomm.ui.button
import fhomm.ui.label
import fhomm.ui.scrollbar


class Toolkit(object):
    def __init__(self, loader, pal_name):
        self.loader = loader
        self.palette = self.load_palette(pal_name)

        self.font = None
        self.hl_font = None
        self.small_font = None
        self.button_font = None
        self.pressed_button_font = None

    def get_palette(self):
        return self.palette

    def get_font(self):
        if self.font is None:
            self.font = self.load_font(
                'font.icn',
                baseline=11,
                space_width=6,
            )
        return self.font

    def get_hl_font(self):
        if self.hl_font is None:
            self.hl_font = self.load_font(
                'font.icn',
                baseline=11,
                space_width=6,
                color=232,
            )
        return self.hl_font

    def get_small_font(self):
        if self.small_font is None:
            self.small_font = self.load_font(
                'smalfont.icn',
                baseline=6,
                space_width=4,
            )
        return self.small_font

    def get_button_font(self):
        if self.button_font is None:
            self.button_font = ButtonFont(self, is_pressed=False)

        return self.button_font

    def get_pressed_button_font(self):
        if self.pressed_button_font is None:
            self.pressed_button_font = ButtonFont(self, is_pressed=True)

        return self.pressed_button_font

    def load_palette(self, pal_name):
        pal = self.loader.load_pal(pal_name)
        return [
            (
                4*pal[i*3],
                4*pal[i*3+1],
                4*pal[i*3+2],
            )
            for i in range(256)
        ]

    def load_image(self, bmp_name):
        bmp = self.loader.load_bmp(bmp_name)
        return fhomm.render.Image.from_bmp(bmp, self.palette)

    def load_sprite(self, icn_name, idx):
        return fhomm.render.Sprite.from_icn_sprite(
            self.loader.load_icn(icn_name)[idx],
            self.palette,
        )

    def load_all_sprites(self, icn_name):
        return [
            fhomm.render.Sprite.from_icn_sprite(
                icn_sprite,
                self.palette,
            )
            for icn_sprite in self.loader.load_icn(icn_name)
        ]

    def load_font(self, icn_name, color=None, **kwargs):
        icns = self.loader.load_icn(icn_name)
        if color is not None:
            icns = [
                fhomm.resource.icn.recolor_sprite(
                    icn,
                    b'\xff',
                    bytes.fromhex('%02x' % color),
                )
                for icn in icns
            ]
        sprites = [
            fhomm.render.Sprite.from_icn_sprite(icn, self.palette)
            for icn in icns
        ]
        return fhomm.render.font.Font(sprites, **kwargs)

    def label(self, size, text):
        return fhomm.ui.label.Label(size, self.get_font(), text)

    def dynamic_label(self, size, text_fn):
        return fhomm.ui.label.DynamicLabel(size, self.get_font(), text_fn)

    def icon(self, icn_name, idx, **kwargs):
        return fhomm.ui.element.ActiveIcon(
            self.load_sprite(icn_name, idx),
            **kwargs,
        )

    def button(self, icn_name, base_idx, **kwargs):
        return fhomm.ui.button.Button(
            self.load_sprite(icn_name, base_idx),
            self.load_sprite(icn_name, base_idx + 1),
            **kwargs,
        )

    def list(self, size, items, img_size, **kwargs):
        return fhomm.ui.list.List(
            size, self.get_font(), self.get_hl_font(), items, img_size, **kwargs,
        )

    def scrollbar(self, size, **kwargs):
        return fhomm.ui.scrollbar.ScrollBar(
            size,
            self.load_sprite('scroll.icn', 4),
            **kwargs,
        )
