import random
from Things import *


class Colony:

    def __init__(self, world, pos, id):

        if pos is None:
            pos = random.sample(world.non_ocean, 1)[0].position
        self.position = pos
        self.color = (random.randrange(255), random.randrange(255), random.randrange(255))
        self.id = id

        self.spawn_rate = 10
        self.timer = 0

    def spawn(self, things, world):

        self.timer += 1
        if self.timer >= self.spawn_rate:
            self.timer = 0
            things.append(Soldier(world, self.position.copy(), self.id))
            things[-1].color = self.color