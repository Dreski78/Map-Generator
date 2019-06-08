import numpy as np

from generate_map import Map
from Things import *
import pygame
from pygame.locals import *

if __name__ == '__main__':

    WIDTH = 1600
    HEIGHT = 900
    cell_size = 8
    thing_size = 5

    MAX_THINGS = ((HEIGHT // cell_size) * (WIDTH // cell_size))
    MAX_THINGS *= .04
    MAX_THINGS = int(MAX_THINGS)
    print("Max Things: ", MAX_THINGS)

    world = Map(WIDTH, HEIGHT, cell_size)

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    starting_things = [Thing(world, None, thing_size) for i in range(5)]

    living_things = []
    living_things += starting_things

    clock = pygame.time.Clock()
    camera_offset = [0, 0]
    scale_offset = 1

    font = pygame.font.Font(None, 30)

    for cell in world.cells:
        pygame.draw.rect(screen, cell.color,
                         (((cell.position[0] + camera_offset[0]) * cell_size) * scale_offset,
                          ((cell.position[1] + camera_offset[1]) * cell_size) * scale_offset,
                          cell_size * scale_offset,
                          cell_size * scale_offset))

    print("Done loading!")

    while True:

        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    scale_offset += .5
                    screen.fill((0, 0, 255))
                elif event.button == 5:
                    scale_offset -= .5
                    screen.fill((0, 0, 255))

        keys = pygame.key.get_pressed()

        if keys[K_a]:
            camera_offset[0] += 1
        if keys[K_d]:
            camera_offset[0] -= 1
        if keys[K_w]:
            camera_offset[1] += 1
        if keys[K_s]:
            camera_offset[1] -= 1

        for cell in world.affected_cells:
            pygame.draw.rect(screen, cell.color,
                             (((cell.position[0] + camera_offset[0]) * cell_size) * scale_offset,
                              ((cell.position[1] + camera_offset[1]) * cell_size) * scale_offset,
                              cell_size * scale_offset,
                              cell_size * scale_offset))

        world.affected_cells = []

        for thing in living_things:
            thing.update(world)
            pygame.draw.rect(screen, thing.color,
                             ((thing.position[0] + camera_offset[0]) * scale_offset,
                              (thing.position[1] + camera_offset[1]) * scale_offset,
                              thing_size * scale_offset,
                              thing_size * scale_offset))

        if len(living_things) > MAX_THINGS:
            for thing in random.sample(living_things, len(living_things) - MAX_THINGS):
                world.grid[thing.position[0]][thing.position[1]].contains.remove(thing)
                living_things.remove(thing)

        fps = font.render(str(int(clock.get_fps())), True, pygame.Color('white'))
        count = font.render(str(int(len(world.affected_cells))), True, pygame.Color('white'))
        screen.fill((0, 0, 255), (0, 0, 60, 40))
        screen.blit(fps, (0, 0))
        screen.blit(count, (0, 20))




        pygame.display.flip()
