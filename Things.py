import numpy as np
import random


class Thing:

    def __init__(self, world, pos, size):
        if pos is None:
            pos = random.sample(world.non_ocean, 1)[0].position
        self.position = [pos[0] * world.cell_size, pos[1] * world.cell_size]
        self.color = (255, 0, 0)
        self.size = size
        self.speed = 5
        self.velocity = [random.uniform(-4, 4), random.uniform(-4, 4)]
        self.triangulate(world).contains.append(self)
        self.random_move = 0

    def update(self, world):
        self.move(world)
        pass

    def move(self, world):
        self.random_move += 1
        if self.random_move >= 300:
            self.random_move = 0
            self.velocity = [random.uniform(-4, 4), random.uniform(-4, 4)]

        self.triangulate(world).contains.remove(self)

        scale = abs(self.velocity[0]) + abs(self.velocity[1])
        if scale == 0:
            scale = .1

        newposx = self.position[0] + int((self.velocity[0] / scale) * self.speed)
        newposy = self.position[1] + int((self.velocity[1] / scale) * self.speed)
        newpos = [newposx, newposy]
        if self.triangulate(world, newpos).is_water:
            if self.triangulate(world, newpos).position[1] == self.triangulate(world).position[1]:
                self.velocity[0] = -self.velocity[0]
            else:
                self.velocity[1] = -self.velocity[1]
        else:
            self.position = newpos

        self.triangulate(world).contains.append(self)
        _ = [world.affected_cells.append(thing) for thing in self.triangulate(world).get_neighbors(1, world.grid)]

    def triangulate(self, world, pos=None):
        if pos is None:
            pos = [self.position[0] // world.cell_size, self.position[1] // world.cell_size]
        else:
            pos = [pos[0] // world.cell_size, pos[1] // world.cell_size]
        return world.grid[pos[0]][pos[1]]

    def conclude(self, *args):
        pass


class Prey(Thing):

    def __init__(self, map, pos):
        super().__init__(map, pos, 5)
        self.color = (0, 255, 255)
        self.hp = random.randrange(0, 50)

    def update(self, world):
        self.move(world)
        self.hp += 1

    def conclude(self, world, living_things):
        if self.hp >= 50:
            self.hp = 0
            living_things.append(Prey(world, self.position.copy()))


class Predator(Thing):

    def __init__(self, map, pos):
        super().__init__(map, pos, 5)
        self.color = (255, 0, 0)
        self.hp = 50

    def update(self, world):
        self.move(world)
        self.hp -= 1

    def conclude(self, world, living_things):
        if self.hp <= 0:
            living_things.remove(self)
            world.grid[self.position[0]][self.position[1]].contains.remove(self)


class Soldier(Thing):

    def __init__(self, world, pos, size, id):
        super().__init__(world, pos, size)

        self.hp = 100
        self.strength = random.randrange(25)

        self.id = id
        self.scan_radius = 4
        self.current_target = None
        self.timeout = 0

    def closest(self, others):
        min = 10000
        min_cell = None
        for other in others:
            pos = abs(other.position[0] - self.position[0]) + abs(other.position[1] - self.position[1])
            if pos < min:
                min = pos
                min_cell = other
        return min_cell

    def update(self, world):
        target = self.scan(world)
        if target:
            target = self.closest(target)
            if target is self.current_target:
                self.timeout += 1
                if self.timeout >= 120:
                    self.velocity = [random.randint(-4, 4), random.randint(-4, 4)]
                    self.timeout = 0
            else:
                self.timeout = 0
            self.current_target = target
            self.velocity = [target.position[0] - self.position[0], target.position[1] - self.position[1]]
        else:
            if self.velocity[0] == 0 and self.velocity[1] == 0:
                self.velocity = [random.randint(-4, 4), random.randint(-4, 4)]
        self.move(world)

    def scan(self, world):

        target = []
        cell = self.triangulate(world)
        for row in range(cell.position[0] - self.scan_radius, cell.position[0] + self.scan_radius + 1):
            for col in range(cell.position[1] - self.scan_radius, cell.position[1] + self.scan_radius + 1):
                try:
                    if world.grid[row][col].contains:
                        for thing in world.grid[row][col].contains:
                            if thing.id != self.id:
                                target.append(thing)

                except:
                    pass

        return target


class Scout(Thing):

    def __init__(self, world, pos, size, id):
        super().__init__(world, pos, size)

        self.hp = 100
        self.strength = random.randrange(25)

        self.id = id
        self.scan_radius = 4
        self.current_target = None
        self.timeout = 0

    def closest(self, others):
        min = 10000
        min_cell = None
        for other in others:
            pos = abs(other.position[0] - self.position[0]) + abs(other.position[1] - self.position[1])
            if pos < min:
                min = pos
                min_cell = other
        return min_cell

    def update(self, world):
        target = self.scan(world)
        if target:
            target = self.closest(target)
            if target is self.current_target:
                self.timeout += 1
                if self.timeout >= 120:
                    self.velocity = [random.randint(-4, 4), random.randint(-4, 4)]
                    self.timeout = 0
            else:
                self.timeout = 0
            self.current_target = target
            self.velocity = [target.position[0] - self.position[0], target.position[1] - self.position[1]]
        else:
            if self.velocity[0] == 0 and self.velocity[1] == 0:
                self.velocity = [random.randint(-4, 4), random.randint(-4, 4)]
        self.move(world)

    def scan(self, world):

        target = []
        cell = self.triangulate(world)
        for row in range(cell.position[0] - self.scan_radius, cell.position[0] + self.scan_radius + 1):
            for col in range(cell.position[1] - self.scan_radius, cell.position[1] + self.scan_radius + 1):
                try:
                    if world.grid[row][col].resources:
                        for resource in world.grid[row][col].resources:
                                target.append(resource)

                except:
                    pass

        return target
