import os
import pygame

import fhomm.agg
import fhomm.bmp
import fhomm.pal


def make_sdl_palette(palette):
    return [
        (
            4*palette[i*3],
            4*palette[i*3+1],
            4*palette[i*3+2],
        )
        for i in range(256)
    ]


with open('/home/ash/Downloads/homm/data/HEROES.AGG', 'rb') as f:
    entries = fhomm.agg.read_entries(f)

    palette = fhomm.pal.read_palette(f, entries)

    heroesbmp = entries['heroes.bmp']
    f.seek(heroesbmp.offset, os.SEEK_SET)
    heroes = fhomm.bmp.read_bitmap(f)


pygame.init()
screen = pygame.display.set_mode((640, 480))

sdl_palette = make_sdl_palette(palette)

s = pygame.image.frombuffer(heroes.data, (heroes.width, heroes.height), 'P')
s.set_palette(sdl_palette)

clock = pygame.time.Clock()
running = True
dt = 0

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(s, (0, 0))

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    dt = clock.tick(60)  # limits FPS to 60

pygame.quit()
