import fhomm.agg


def read_palette(aggf, resources):
    kbpal = resources['kb.pal']
    if 768 != kbpal.size:
        raise Exception(f"Expected the palette chunk to have 768 bytes, but got: {kbpal.size}")

    return fhomm.agg.read_entry_data(aggf, kbpal)
