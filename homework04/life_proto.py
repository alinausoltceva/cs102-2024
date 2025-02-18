import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        # PUT YOUR CODE HERE
        self.create_grid(randomize=True)
        running = True
        while running:
            # print(123)
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            self.draw_grid()
            self.draw_lines()
            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)

            # PUT YOUR CODE HERE

            pygame.display.flip()
            clock.tick(self.speed)
            self.get_next_generation()
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        grid=[]
        if randomize:
            for i in range(0,self.height,self.cell_size):
                grid.append([])
                for j in range(0,self.width,self.cell_size):
                    grid[i//self.cell_size].append(random.choice([0,1]))
        else:
            for i in range(0,self.height,self.cell_size):
                grid.append([])
                for j in range(0,self.width,self.cell_size):
                    grid[i//self.cell_size].append(0)
        self.grid=grid
        return grid
        pass

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for w in range(0, self.width, self.cell_size):
            for h in range(0, self.height, self.cell_size):
                # print(w//self.cell_size,h//self.cell_size)
                if self.grid[h // self.cell_size][w // self.cell_size] == 1:
                    pygame.draw.rect(
                        self.screen, pygame.Color("green"), (w, h, self.cell_size, self.cell_size)
                    )
                else:
                    pygame.draw.rect(
                        self.screen, pygame.Color("white"), (w, h, self.cell_size, self.cell_size)
                    )
        pass

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        neib=[]
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if i==j==0:
                    continue
                elif cell[0]==0 and i==-1:
                    continue
                elif cell[0]+1==self.height//self.cell_size and i==1:
                    continue
                elif cell[1]==0 and j==-1:
                    continue
                elif cell[1]+1==self.width//self.cell_size and j==1:
                    continue
                neib.append(self.grid[cell[0]+i][cell[1]+j])
        return neib
        pass

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        next_generation=[]
        for i in range(0,self.height//self.cell_size):
            next_generation.append([])
            for j in range(self.width//self.cell_size):
                neighbours=self.get_neighbours((i,j))
                if self.grid[i][j]==1 and sum(neighbours) in  [2,3]:
                    next_generation[i].append(1)
                elif self.grid[i][j]==0 and sum(neighbours)==3:
                    next_generation[i].append(1)
                else:
                    next_generation[i].append(0)
        self.grid=next_generation
        return next_generation
        pass


if __name__ == "__main__":
    game=GameOfLife()
    game.run()