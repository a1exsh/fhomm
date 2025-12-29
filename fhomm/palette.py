class Palette(object):
    def __init__(self, palette, cycle_ticks=250):
        self.palette = palette
        self.tick = 0
        self.cycle_ticks = cycle_ticks

    def update_tick(self, dt):
        cycled = False

        self.tick += dt
        while self.tick >= self.cycle_ticks:
            self.palette = cycle(self.palette)
            cycled = True
            self.tick -= self.cycle_ticks

        return cycled


def cycle(palette):
    return [
        palette[cycle_index(i)]
        for i in range(len(palette))
    ]


def cycle_index(i):
    if i < 224:
        return i
    elif i < 228:
        return cycle_for_span(224, 4, i)
    elif i < 232:
        return cycle_for_span(228, 4, i)
    elif i < 240:
        return i
    elif i < 245:
        return cycle_for_span(240, 5, i)
    elif i < 251:
        return cycle_for_span(245, 6, i)
    else:
        return i


def cycle_for_span(start, size, i):
    return start + ((i - start) + 1) % size


def make_safe_for_shadow(palette):
    palette = list(palette)     # make an assignable copy
    palette[224:232] = [(255, 255, 255)]*8
    palette[240:251] = [(255, 255, 255)]*11
    return palette
