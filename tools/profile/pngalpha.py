"""Stdlib PNG alpha probe: does a logo have real transparency, and is it too dark to sit on the dark card?"""
import struct, zlib

def stats(path):
    """(transparent_fraction, dark_fraction_of_opaque) for 8-bit RGBA PNGs; None for anything else."""
    b = path.read_bytes(); i, idat = 8, b""
    while i < len(b):
        n, t = struct.unpack(">I4s", b[i:i+8]); d = b[i+8:i+8+n]; i += 12 + n
        if t == b"IHDR": w, h, bd, ct, _, _, il = struct.unpack(">IIBBBBB", d)
        elif t == b"IDAT": idat += d
    if (bd, ct, il) != (8, 6, 0): return None
    raw, st, prev, p, tr, op, dark = zlib.decompress(idat), w*4, bytearray(w*4), 0, 0, 0, 0
    for _ in range(h):
        ft, line = raw[p], bytearray(raw[p+1:p+1+st]); p += 1 + st
        for x in range(st):
            a = line[x-4] if x >= 4 else 0; u = prev[x]; c = prev[x-4] if x >= 4 else 0
            if ft == 1: line[x] = (line[x] + a) & 255
            elif ft == 2: line[x] = (line[x] + u) & 255
            elif ft == 3: line[x] = (line[x] + ((a + u) >> 1)) & 255
            elif ft == 4:
                pa, pb, pc = abs(u-c), abs(a-c), abs(a+u-2*c)
                line[x] = (line[x] + (a if pa <= pb and pa <= pc else u if pb <= pc else c)) & 255
        for x in range(0, st, 4):
            if line[x+3] < 20: tr += 1
            else:
                op += 1
                if .2126*line[x] + .7152*line[x+1] + .0722*line[x+2] < 50: dark += 1
        prev = line
    return tr/(w*h), dark/max(op, 1)

def floats_on_dark(path):
    """True when the logo is meant for a dark background: real transparency and not mostly-dark artwork."""
    s = stats(path)
    return bool(s) and s[0] >= .15 and s[1] < .8
