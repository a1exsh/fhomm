import os
import fhomm.agg
import fhomm.bmp
import fhomm.icn


class Loader(object):
    def __init__(self, agg):
        self.agg = agg

    def load_pal(self, name):
        pal = self.agg.entries[name]
        if 768 != pal.size:
            raise Exception(f"Expected the palette chunk to have 768 bytes, but got: {pal.size}")

        return fhomm.agg.read_entry_data(self.agg.f, pal)

    def load_bmp(self, name):
        self.seek_to(name)
        return fhomm.bmp.read_bitmap(self.agg.f)

    def load_icn(self, name):
        self.seek_to(name)
        return fhomm.icn.read_icn_sprites(self.agg.f)

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
