import fhomm.resource.agg


def read_palette(agg, pal_name):
    pal = agg.entries[pal_name]
    if 768 != pal.size:
        raise Exception(f"Expected the palette chunk to have 768 bytes, but got: {pal.size}")

    return shift_palette(
        fhomm.resource.agg.read_entry_data(agg.f, pal)
    )


def shift_palette(pal):
    return [
        (
            shlext2(pal[i * 3]),
            shlext2(pal[i * 3 + 1]),
            shlext2(pal[i * 3 + 2]),
        )
        for i in range(256)
    ]


def shlext(x):
    return (x << 1) | (x & 1)


def shlext2(x):
    return shlext(shlext(x))
