import random


class Thing:

    def __init__(self, world, pos):
        if pos is None:
            pos = random.sample(world.non_ocean, 1)[0].position
        self.position = pos
        self.color = (255, 0, 0)
        world.grid[pos[0]][pos[1]].contains.append(self)

    def update(self, world):
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

    def conclude(self, *args):
        pass


class Prey(Thing):

    def __init__(self, map, pos):
        super().__init__(map, pos)
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
        super().__init__(map, pos)
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

    def __init__(self, world, pos, id):
        super().__init__(world, pos)

        self.hp = 100
        self.strength = random.randrange(25)

        self.id = id
        self.scan_radius = 5

    def update(self, world):
        target = self.scan(world)
        if not target:
            self.move(world)
        else:
            self.attack(world, target)

    def scan(self, world):

        target = []
        for row in range(self.position[0] - self.scan_radius, self.position[0] + self.scan_radius + 1):
            for col in range(self.position[1] - self.scan_radius, self.position[1] + self.scan_radius + 1):
                try:
                    if world.grid[row][col].contains:
                        for cell in world.grid[row][col].contains:
                            if cell.id != self.id:
                                target.append(world.grid[row][col])
                except:
                    pass

        return target

    def attack(self, world, targets):

        target = targets[0].position

        world.grid[self.position[0]][self.position[1]].contains.remove(self)

        if self.position[0] != target[0]:
            x = target[0] - self.position[0]
            x /= abs(x)  # normalize
            self.position[0] += int(x)

        if self.position[1] != target[1]:
            y = target[1] - self.position[1]
            y /= abs(y)  # normalize
            self.position[1] += int(y)


        world.grid[self.position[0]][self.position[1]].contains.append(self)
        world.affected_cells.append(world.grid[self.position[0]][self.position[1]])