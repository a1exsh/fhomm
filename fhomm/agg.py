# AGG file decoding
import os
from collections import OrderedDict, namedtuple

import fhomm.io

INDEX_ENTRY_SIZE = 2 + 4 + 4 + 4  # 2-byte "hash" + 4-byte offset + 4-byte size + 4-byte size2
ENTRY_NAME_SIZE = 15

IndexEntry = namedtuple('IndexEntry', ['offset', 'size'])


def read_entry_name(f):
    name = fhomm.io.must_read(f, ENTRY_NAME_SIZE)
    term = name.find(b'\0')
    if term <= 0:
        raise Exception(f"Unexpected null-terminator index in the entry name: {name}")
    return name[:term].decode('utf-8').lower()


def read_index_entry(f):
    fhomm.io.must_read(f, 2)    # ignored for now.  is this some hash code?
    entry = IndexEntry(offset=fhomm.io.read_le32(f), size=fhomm.io.read_le32(f))
    size2 = fhomm.io.read_le32(f)
    if entry.size != size2:
        raise Exception(f"Expected the second size to match the first one, but got {entry.size} != {size2}")
    return entry


def read_entry_data(f, entry):
    f.seek(entry.offset, os.SEEK_SET)
    return fhomm.io.must_read(f, entry.size)


def read_entries(f):
    nitems = fhomm.io.read_le16(f)
    print(f"number of items: {nitems}")

    index_size = nitems * INDEX_ENTRY_SIZE
    index_data = fhomm.io.must_read(f, index_size)

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

    return entries
