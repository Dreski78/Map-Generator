import random
from Things import *


class Colony:

    def __init__(self, world, pos, id, colonies):

        if pos is None:
            pos = random.sample(world.non_ocean, 1)[0]
            Found = False

            while not Found:
                if len(colonies) == 0:
                    Found = True

                count = 0
                for colony in colonies:
                    if pos in colony.get_neighbors(20, world):
                        pos = random.sample(world.non_ocean, 1)[0]
                    else:
                        count += 1

                if count == len(colonies):
                    Found = True

        self.position = pos.position
        self.color = (random.randrange(255), random.randrange(255), random.randrange(255))
        self.id = id
        self.score = 0

        self.spawn_rate = 15
        self.timer = 0

    def get_neighbors(self, reach, world):
        neighbors = []
        for row in range(self.position[0] - reach, self.position[0] + reach + 1):
            for col in range(self.position[1] - reach, self.position[1] + reach + 1):
                try:
                    neighbors.append(world.grid[row][col])
                except:
                    pass
        return neighbors

    def spawn(self, things, world, thing_size):

        self.timer += 1
        if self.timer >= self.spawn_rate:
            self.timer = 0
            things.append(Soldier(world, self.position.copy(), thing_size, self.id))
            things[-1].color = self.color
