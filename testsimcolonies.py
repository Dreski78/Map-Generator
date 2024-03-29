import numpy as np
from colonies import Colony
from generate_map import Map
from Things import *
import pygame
from pygame.locals import *

def resolve(matchup):
    global living_things
    # if all(thing.id for thing in matchup):
    #     return

    for thing in matchup:

        for other in matchup:

            if other.id == thing.id:
                continue

            else:
                other.hp -= thing.strength
                colonies[other.id].score -= thing.strength
                colonies[thing.id].score += thing.strength


    for thing in matchup:
        if thing.hp <= 0:
            living_things.remove(thing)
            matchup.remove(thing)

if __name__ == '__main__':

    WIDTH = 1366
    HEIGHT = 768
    cell_size = 10
    thing_size = 6

    colors = {"Cornflower_blue": (77, 166, 255), "Crimson_glory": (175, 0, 42), "Blue": (0, 120, 255),
              "purple": (189, 0, 255), "orange": (255, 154, 0), "green": (1, 255, 31), "yellow": (227, 255, 0)}

    MAX_THINGS = ((HEIGHT // cell_size) * (WIDTH // cell_size))
    MAX_THINGS *= .04
    MAX_THINGS = int(MAX_THINGS)
    print("Max Things: ", MAX_THINGS)

    world = Map(WIDTH, HEIGHT, cell_size)
    resources = world.resources

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    colonies = []
    colors = random.sample(list(colors.values()), 4)

    for i in range(4):
        colonies.append(Colony(world, None, i, colonies))
        colonies[i].color = colors[i]

    living_things = []

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

        for colony in colonies:
            colony.spawn(living_things, world, thing_size)
            pygame.draw.rect(screen, colony.color,
                             (((colony.position[0] + camera_offset[0]) * cell_size) * scale_offset,
                              ((colony.position[1] + camera_offset[1]) * cell_size) * scale_offset,
                              cell_size * scale_offset * 1.5,
                              cell_size * scale_offset * 1.5))

        for thing in living_things:
            thing.update(world)
            pygame.draw.rect(screen, thing.color,
                             ((thing.position[0] + camera_offset[0]) * scale_offset,
                              (thing.position[1] + camera_offset[1]) * scale_offset,
                              thing_size * scale_offset,
                              thing_size * scale_offset))

        for cell in world.affected_cells:
            if len(cell.contains) > 1:
                resolve(cell.contains)

        # if len(living_things) > MAX_THINGS:
        #     for thing in random.sample(living_things, len(living_things) - MAX_THINGS):
        #         world.grid[thing.position[0]][thing.position[1]].contains.remove(thing)
        #         living_things.remove(thing)

        for resource in resources:
            pygame.draw.circle(screen, resource.color,
                               ((resource.position[0] + camera_offset[0]) * scale_offset,
                                (resource.position[1] + camera_offset[1]) * scale_offset),
                               2 * scale_offset)

        texts = []
        for colony in colonies:
            texts.append(font.render(str(colony.score), True, colony.color))

        screen.fill((0, 0, 255), (0, 0, 60, 120))

        for num, text in enumerate(texts):
            screen.blit(text, (0, num * 20))


        fps = font.render(str(int(clock.get_fps())), True, pygame.Color('white'))
        count = font.render(str(int(len(world.affected_cells))), True, pygame.Color('white'))

        screen.blit(fps, (0, 80))
        screen.blit(count, (0, 100))




        pygame.display.flip()
