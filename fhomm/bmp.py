from collections import namedtuple

import fhomm.io

Bitmap = namedtuple('Bitmap', ['width', 'height', 'data'])


def read_bitmap(f):
    fhomm.io.must_read(f, 2)    # ignored for now, meaning unknown
    width = fhomm.io.read_le16(f)
    height = fhomm.io.read_le16(f)
    return Bitmap(width, height, fhomm.io.must_read(f, width*height))
