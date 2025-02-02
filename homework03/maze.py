from copy import deepcopy
from random import choice, randint, seed
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(
        grid: List[List[Union[str, int]]], coord: Tuple[int, int]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """
    # x - вертикаль
    # y - горизонталь

    x, y, rows, cols = coord[0], coord[1], len(grid) - 1, len(grid[0]) - 1
    directions = ["up", "right"]
    direction = choice(directions)
    if direction == "up" and (0 <= x - 2 < rows and 0 <= y < cols):
        grid[x - 1][y] = " "
    else:
        direction = "right"
    if direction == "right" and (0 <= x < rows and 0 <= y + 2 < cols):
        grid[x][y + 1] = " "
    elif 0 <= x - 2 < rows and 0 <= y < cols:
        grid[x - 1][y] = " "

    return grid


def bin_tree_maze(
        rows: int = 15, cols: int = 15, random_exit: bool = True
) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки
    for x in range(1, rows - 1):
        for y in range(1, cols - 1):
            if x % 2 == y % 2 == 1:
                remove_wall(grid, (x, y))
    # генерация входа и выхода
    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """
    maxy = len(grid[0])
    maxx = len(grid)
    first = None
    second = None
    for x in range(maxx):
        for y in range(maxy):
            if grid[x][y] == "X":
                if first is None:
                    first = (x, y)
                else:
                    second = (x, y)
    if first is None:
        return []
    if second is None:
        return [first]
    return [first, second]
    pass


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == k:
                if i + 1 < len(grid) and grid[i + 1][j] == 0:
                    grid[i + 1][j] = k + 1
                if i - 1 >= 0 and grid[i - 1][j] == 0:
                    grid[i - 1][j] = k + 1
                if j - 1 >= 0 and grid[i][j - 1] == 0:
                    grid[i][j - 1] = k + 1
                if j + 1 < len(grid[0]) and grid[i][j + 1] == 0:
                    grid[i][j + 1] = k + 1

    return grid


def shortest_path(
        grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """
    grid_copy = deepcopy(grid)
    max_k = grid_copy[exit_coord[0]][exit_coord[1]]
    step_ = max_k
    steps = [(exit_coord[0], exit_coord[1])]
    coords = [exit_coord[0], exit_coord[1]]
    while step_ > 1:
        if coords[0] + 1 < len(grid) and grid_copy[coords[0] + 1][coords[1]] == step_ - 1:
            steps.append((coords[0] + 1, coords[1]))
            coords = (coords[0] + 1, coords[1])
            step_ -= 1
        elif coords[0] - 1 >= 0 and grid_copy[coords[0] - 1][coords[1]] == step_ - 1:
            steps.append((coords[0] - 1, coords[1]))
            coords = (coords[0] - 1, coords[1])
            step_ -= 1
        if coords[1] + 1 < len(grid[0]) and grid_copy[coords[0]][coords[1] + 1] == step_ - 1:
            steps.append((coords[0], coords[1] + 1))
            coords = (coords[0], coords[1] + 1)
            step_ -= 1
        elif coords[1] - 1 >= 0 and grid_copy[coords[0]][coords[1] - 1] == step_ - 1:
            steps.append((coords[0], coords[1] - 1))
            coords = (coords[0], coords[1] - 1)
            step_ -= 1
    # steps.append((enter[0], enter[1]))
    return steps
    pass


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """
    maxy = len(grid[0])
    maxx = len(grid)

    if coord[0] in [0, maxx - 1] and coord[1] in [0, maxy - 1]:
        return True
    else:
        if coord[0] == 0:
            if grid[coord[0]][coord[1] + 1] == "■" and grid[coord[0]][coord[1] - 1] == "■" and \
                    grid[coord[0] + 1][
                        coord[1]] == "■":
                return True
        elif coord[0] == maxx - 1:
            if grid[coord[0]][coord[1] + 1] == "■" and grid[coord[0]][coord[1] - 1] == "■" and \
                    grid[coord[0] - 1][
                        coord[1]] == "■":
                return True
        elif coord[1] == 0:
            if grid[coord[0] + 1][coord[1]] == "■" and grid[coord[0] - 1][coord[1]] == "■" and \
                    grid[coord[0]][
                        coord[1] + 1] == "■":
                return True
        elif coord[1] == maxy - 1:
            if grid[coord[0] + 1][coord[1]] == "■" and grid[coord[0] - 1][coord[1]] == "■" and \
                    grid[coord[0]][
                        coord[1] - 1] == "■":
                return True
    return False


def solve_maze(
        grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """

    :param grid:
    :return:
    """
    grid_copy = deepcopy(grid)
    exits = get_exits(grid)
    if len(exits) == 1:
        return grid, exits[0]
    else:
        if encircled_exit(grid, exits[0]) or encircled_exit(grid, exits[1]):
            return grid, None
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid_copy[i][j] == " ":
                grid_copy[i][j] = 0
    enter, exit = exits
    grid_copy[enter[0]][enter[1]] = 1
    grid_copy[exit[0]][exit[1]] = 0
    i = 1
    while grid_copy[exit[0]][exit[1]] == 0:
        make_step(grid_copy, i)
        i += 1
    steps = shortest_path(grid_copy, exit)
    return grid, steps
    pass


def add_path_to_grid(
        grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
