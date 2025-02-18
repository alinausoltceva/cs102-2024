import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
            self,
            size: tp.Tuple[int, int],
            randomize: bool = True,
            max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        # Copy from previous assignment
        grid = []
        if randomize:
            for i in range(0, self.rows):
                grid.append([])
                for j in range(0, self.cols):
                    grid[i].append(random.choice([0, 1]))
        else:
            for i in range(0, self.rows):
                grid.append([])
                for j in range(0, self.cols):
                    grid[i].append(0)
        return grid
        pass

    def get_neighbours(self, cell: Cell) -> Cells:
        # Copy from previous assignment
        neib = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == j == 0:
                    continue
                elif cell[0] == 0 and i == -1:
                    continue
                elif cell[0] + 1 == self.rows and i == 1:
                    continue
                elif cell[1] == 0 and j == -1:
                    continue
                elif cell[1] + 1 == self.cols and j == 1:
                    continue
                neib.append(self.curr_generation[cell[0] + i][cell[1] + j])
        return neib
        pass

    def get_next_generation(self) -> Grid:
        # Copy from previous assignment
        next_generation = []
        for i in range(0, self.rows):
            next_generation.append([])
            for j in range(self.cols):
                neighbours = self.get_neighbours((i, j))
                if self.curr_generation[i][j] == 1 and sum(neighbours) in [2, 3]:
                    next_generation[i].append(1)
                elif self.curr_generation[i][j] == 0 and sum(neighbours) == 3:
                    next_generation[i].append(1)
                else:
                    next_generation[i].append(0)
        # self.grid = next_generation
        return next_generation
        pass

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        next_gen = self.get_next_generation()
        self.prev_generation = self.curr_generation
        self.curr_generation = next_gen
        self.generations += 1
        pass

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.max_generations == self.generations
        pass

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        changes = False
        for i in range(self.rows):
            for j in range(self.cols):
                changes = changes or (self.curr_generation[i][j] != self.prev_generation[i][j])
        return changes
        pass

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        grid = []
        with open(filename, 'w') as f:
            for line in f:
                grid.append([int(cell) for cell in line.strip()])
        game = GameOfLife((len(grid), len(grid[0])), randomize=False, max_generations=float("inf"))
        game.curr_generation = grid
        return game
        pass

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, 'w') as f:
            for row in self.curr_generation:
                f.write(''.join(str(cell) for cell in row) + '\n')
        pass
