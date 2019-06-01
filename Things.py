import random


class Thing:

    def __init__(self, map, pos):
        if pos is None:
            pos = random.sample(map.non_ocean, 1)[0].position
        self.position = pos
        self.color = (255, 0, 0)
        map.grid[pos[0]][pos[1]].contains.append(self)


    def step(self, world):
        self.move(world)
        pass

    def move(self, world):
        direction = random.randrange(4)
        world.grid[self.position[0]][self.position[1]].contains.remove(self)

        if direction == 0:
            if not world.grid[self.position[0] + 1][self.position[1]].is_water:
                self.position[0] += 1
        elif direction == 1:
            if not world.grid[self.position[0] - 1][self.position[1]].is_water:
                self.position[0] -= 1
        elif direction == 2:
            if not world.grid[self.position[0]][self.position[1] + 1].is_water:
                self.position[1] += 1
        elif direction == 3:
            if not world.grid[self.position[0]][self.position[1] - 1].is_water:
                self.position[1] -= 1

        world.grid[self.position[0]][self.position[1]].contains.append(self)
        world.affected_cells.append(world.grid[self.position[0]][self.position[1]])


class Prey(Thing):

    def __init__(self, map, pos):
        super().__init__(map, pos)
        self.color = (0, 255, 255)
        self.hp = random.randrange(0, 50)

    def step(self, world):
        self.move(world)
        self.hp += 1

    def conclude(self, world, living_things):
        if self.hp >= 50:
            self.hp = 0
            living_things.append(Prey(world, self.position.copy()))


class Predator(Thing):

    def __init__(self, map, pos):
        super().__init__(map, pos)
        self.color = (255, 0, 0)
        self.hp = 50

    def step(self, world):
        self.move(world)
        self.hp -= 1

    def conclude(self, world, living_things):
        if self.hp <= 0:
            living_things.remove(self)
            world.grid[self.position[0]][self.position[1]].contains.remove(self)
