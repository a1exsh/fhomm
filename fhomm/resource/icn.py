import os
import io
from collections import namedtuple

import fhomm.io

SpriteHeader = namedtuple(
    'SpriteHeader',
    ['offx', 'offy', 'width', 'height', 'data_start']
)

Sprite = namedtuple(
    'Sprite',
    ['offx', 'offy', 'width', 'height', 'data']
)


def read_icn_sprites(f):
    nsprites = fhomm.io.read_le16(f)
    total_size = fhomm.io.read_le32(f)

    start = f.tell()

    headers = []
    for i in range(nsprites):
        headers.append(read_sprite_header(f))

    sprites = []
    for h in headers:
        f.seek(start + h.data_start, os.SEEK_SET)
        sprites.append(
            Sprite(h.offx, h.offy, h.width, h.height, read_sprite_data(f, h))
        )

    return sprites


def read_sprite_header(f):
    return SpriteHeader(
        fhomm.io.read_signed_le16(f),
        fhomm.io.read_signed_le16(f),
        fhomm.io.read_le16(f),
        fhomm.io.read_le16(f),
        fhomm.io.read_le32(f),
    )


def read_sprite_data(f, h):
    with io.BytesIO() as data:
        x = 0                   # tracks position in the row currently read
        while True:
            n = fhomm.io.read_byte(f)
            # print(f"read: {n}")
            if n == 0:          # end of row
                # fill to the end of the row
                skip = h.width - x
                # print(f"end of row => filling {skip}")
                data.write(b'\x00'*skip)
                x = 0

            elif n < 0x80:      # read next N pixels
                data.write(fhomm.io.must_read(f, n))
                x += n

            elif n == 0x80:     # end of sprite
                return data.getvalue()

            else:               # skip (N - 0x80) transparent pixels
                skip = n - 0x80
                # print(f"transparency => filling {skip}")
                data.write(b'\x00'*skip)
                x += skip
