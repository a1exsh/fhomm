import os
import fhomm.resource.agg
import fhomm.resource.bmp
import fhomm.resource.icn
import fhomm.resource.pal


def get_icn_class(name):
    if name in ["font.icn", "smalfont.icn"]:
        return fhomm.resource.icn.ALL_MONO

    else:
        return fhomm.resource.icn.ALL_COLOR


class AggResourceLoader(object):
    def __init__(self, agg):
        self.agg = agg

    def load_pal(self, name):
        return fhomm.resource.pal.read_palette(self.agg, name)

    def load_bmp(self, name):
        self.seek_to(name)
        return fhomm.resource.bmp.read_bitmap(self.agg.f)

    def load_icn(self, name):
        self.seek_to(name)
        return fhomm.resource.icn.read_icn_sprites(
            self.agg.f,
            get_icn_class(name),
        )

    def seek_to(self, name):
        self.agg.f.seek(self.agg.entries[name].offset, os.SEEK_SET)


class CachingLoader(object):
    def __init__(self, loader):
        self.loader = loader
        self.cache = {}

    def load_pal(self, name):
        return self.load_cached(self.loader.load_pal, name)

    def load_bmp(self, name):
        return self.load_cached(self.loader.load_bmp, name)

    def load_icn(self, name):
        return self.load_cached(self.loader.load_icn, name)

    def load_cached(self, load, name):
        res = self.cache.get(name)
        if res is None:
            res = load(name)
            self.cache[name] = res
        return res
