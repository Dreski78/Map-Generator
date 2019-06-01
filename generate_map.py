import random

import pygame


class Cell:

    def __init__(self, pos):

        self.position = pos
        self.height = None
        self.color = 0
        self.is_water = False
        self.contains = []

    def __iter__(self):
        return len(self.contains) > 1

    def get_neighbors(self, reach, cells):

        neighbors = []
        for row in range(self.position[0] - reach, self.position[0] + reach + 1):
            for col in range(self.position[1] - reach, self.position[1] + reach + 1):
                try:
                    if cells[row][col].height is not None:
                        neighbors.append(cells[row][col])
                except:
                    pass

        # for cell in cells:
        #     if self.position[0] - reach <= cell.position[0] <= self.position[0] + reach and \
        #             self.position[1] - reach <= cell.position[1] <= reach + self.position[1] and \
        #             cell.height:
        #         neighbors.append(cell)
        return neighbors


class Map:

    def __init__(self, w, h, cell_size):
        self.width = w // cell_size
        self.height = h // cell_size
        self.grid = [[Cell([x, y]) for y in range(self.height)] for x in range(self.width)]
        self.cells = [cell for row in self.grid for cell in row]
        self.make_ocean()
        self.set_levels()
        self.set_color()
        self.non_ocean = [cell for cell in self.cells if cell.is_water is False]
        self.affected_cells = []
        print(len(self.cells))
        print(len(self.non_ocean))

    def make_ocean(self):
        wmin = 0 + self.width // 50
        hmin = 0 + self.height // 50
        wmax = self.width - self.width // 50
        print(wmax)
        hmax = self.height - self.height // 50
        for cell in self.cells:
            if cell.position[0] <= wmin:
                cell.height = random.randint(0, 49)
            if cell.position[0] >= wmax - 1:
                cell.height = random.randint(0, 49)
            if cell.position[1] <= hmin:
                cell.height = random.randint(0, 49)
            if cell.position[1] >= hmax - 1:
                cell.height = random.randint(0, 49)

    def set_levels(self):
        random.shuffle(self.cells)
        for num, cell in enumerate(self.cells):
            if num % 1000 == 0:
                print(f"{num/len(self.cells)*100:.2f}%")
            if cell.height is None:

                for reach in range(1, self.width//10):
                    neighbors = cell.get_neighbors(reach, self.grid)
                    # print(reach, len(neighbors))
                    if not neighbors:
                        continue
                    change_rate = reach * 1.005
                    break

                if not neighbors:
                    cell.height = random.randint(50, 189)
                    continue

                total = 0
                for n in neighbors:
                    total += n.height

                mean = (total / len(neighbors))
                if mean > 160:
                    final = mean + random.uniform(-change_rate * 1.5, change_rate)
                elif mean < 40:
                    final = mean + random.uniform(-change_rate, change_rate * 1.5)
                else:
                    final = mean + random.uniform(-change_rate, change_rate)
                if final > 199:
                    final = 199
                elif final < 0:
                    final = 0

                cell.height = final

    def set_color(self):

        for cell in self.cells:
            if cell.height <= 65:
                cell.color = (0, 0, 255)
                cell.is_water = True
            elif cell.height <= 75:
                cell.color = (0, 100, 255)
            elif cell.height <= 85:
                cell.color = (200, 200, 125)
            elif cell.height <= 150:
                cell.color = (40, 200, 40)
            elif cell.height <= 180:
                cell.color = (125, 255, 125)
            elif cell.height > 180:
                cell.color = (215, 255, 215)



if __name__ == '__main__':

    WIDTH, HEIGHT = 720, 480
    cell_size = 1
    map = Map(WIDTH // cell_size, HEIGHT // cell_size)

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    clock = pygame.time.Clock()

    screen.fill((0, 0, 0))

    for cell in map.cells:
        pygame.draw.rect(screen, cell.color,
                         (cell.position[0] * cell_size, cell.position[1] * cell_size, cell_size, cell_size))

    while True:

        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()



        pygame.display.flip()
