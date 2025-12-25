import os
from collections import OrderedDict, namedtuple

import pygame

INDEX_ENTRY_SIZE = 2 + 4 + 4 + 4  # 2-byte "hash" + 4-byte offset + 4-byte size + 4-byte size2
ENTRY_NAME_SIZE = 15

IndexEntry = namedtuple('IndexEntry', ['offset', 'size'])


def must_read(f, n):
    b = f.read(n)
    if n != len(b):
        raise Exception(f"Expected to read {n} bytes, but got: {len(b)}")
    return b


def read_le16(f):
    b = must_read(f, 2)
    return (b[1] << 8) | b[0]


def read_le32(f):
    b = must_read(f, 4)
    return (b[3] << 24) | (b[2] << 16) | (b[1] << 8) | b[0]


def read_entry_name(f):
    name = must_read(f, ENTRY_NAME_SIZE)
    term = name.find(b'\0')
    if term <= 0:
        raise Exception(f"Unexpected null-terminator index in the entry name: {name}")
    return name[:term].decode('utf-8').lower()


def read_index_entry(f):
    must_read(f, 2)             # ignored for now.  is this some hash code?
    entry = IndexEntry(offset=read_le32(f), size=read_le32(f))
    size2 = read_le32(f)
    if entry.size != size2:
        raise Exception(f"Expected the second size to match the first one, but got {entry.size} != {size2}")
    return entry


def read_entry_data(f, entry):
    f.seek(entry.offset, os.SEEK_SET)
    return must_read(f, entry.size)


Bitmap = namedtuple('Bitmap', ['width', 'height', 'data'])

def read_bitmap(f):
    must_read(f, 2)             # ignored for now, meaning unknown
    width = read_le16(f)
    height = read_le16(f)
    return Bitmap(width, height, must_read(f, width*height),)


with open('data/HEROES.AGG', 'rb') as f:
    nitems = read_le16(f)
    print(f"number of items: {nitems}")

    index_size = nitems * INDEX_ENTRY_SIZE
    index_data = must_read(f, index_size)

    f.seek(0, os.SEEK_END)
    file_size = f.tell()
    print(f"file size: {file_size}")

    f.seek(-nitems * ENTRY_NAME_SIZE, os.SEEK_END)
    toc_start = f.tell()
    print(f"entry names (TOC) starts at {toc_start}")

    entries = OrderedDict()
    for i in range(nitems):
        name = read_entry_name(f)
        # print(name)
        if name in entries:
            raise Exception(f"Entry with this name already seen earlier: {name}")
        entries[name] = IndexEntry(offset=-1, size=-1)

    # print(entries)

    f.seek(2, os.SEEK_SET)
    for name, entry in entries.items():
        entries[name] = read_index_entry(f)

    kbpal = entries['kb.pal']
    if 768 != kbpal.size:
        raise Exception(f"Expected the palette chunk to have 768 bytes, but got: {kbpal.size}")

    palette = read_entry_data(f, kbpal)
    # print(palette)

    heroesbmp = entries['heroes.bmp']
    f.seek(heroesbmp.offset, os.SEEK_SET)
    heroes = read_bitmap(f)


pygame.init()
screen = pygame.display.set_mode((640, 480))

s = pygame.image.frombuffer(heroes.data, (heroes.width, heroes.height), 'P')
pal = [(4*palette[i*3], 4*palette[i*3+1], 4*palette[i*3+2]) for i in range(256)]
#print(pal)
s.set_palette(pal)

screen.blit(s, (0, 0))
pygame.display.flip()
