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
