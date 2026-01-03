import fhomm.render
import fhomm.ui


class Toolkit(object):
    def __init__(self, loader, pal_name):
        self.loader = loader
        self.palette = self.load_palette(pal_name)

        self.font = None
        self.hl_font = None
        self.small_font = None

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
        return fhomm.render.Font(sprites, **kwargs)

    def icon(self, icn_name, idx, **kwargs):
        return fhomm.ui.ActiveIcon(self.load_sprite(icn_name, idx), **kwargs)

    def button(self, icn_name, base_idx, **kwargs):
        return fhomm.ui.Button(
            self.load_sprite(icn_name, base_idx),
            self.load_sprite(icn_name, base_idx + 1),
            **kwargs,
        )
