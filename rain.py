import random
import pygame


class Rain:

    def __init__(self, pos):

        self.vel = random.randrange(10, 30)
        self.pos = pos
        self.color = (random.randrange(255),
                      random.randrange(255),
                      random.randrange(255))

    def fall(self):
        self.pos[1] += self.vel



def create_rain(amount):
    for i in range(amount):
        active_rain.append(Rain([random.randrange(WIDTH), 0]))


WIDTH = 1366
HEIGHT = 768

active_rain = []

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

screen.fill((0, 0, 0))

while True:

    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    screen.fill((0, 0, 0))

    create_rain(4)
    for rain in active_rain:
        rain.fall()
        pygame.draw.rect(screen, rain.color, (rain.pos[0], rain.pos[1], 2, 20))
        if rain.pos[1] > HEIGHT:
            active_rain.remove(rain)


    pygame.display.flip()
