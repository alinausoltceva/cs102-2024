import pathlib
import typing as tp

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """ Прочитать Судоку из указанного файла """
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку """
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов
    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    grid = []
    for i in range(n):
        grid.append([])
        for j in range(n):
            grid[i].append(values[i * n + j])
    return grid
    pass


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos
    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    res = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if i == pos[0]:
                res.append(grid[i][j])
    return res
    pass


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos
    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    res = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if j == pos[1]:
                res.append(grid[i][j])
    return res
    pass


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos
    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    res = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if i // 3 == pos[0] // 3 and j // 3 == pos[1] // 3:
                res.append(grid[i][j])
    return res
    pass


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    """Найти первую свободную позицию в пазле
    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == ".":
                return i, j
    pass


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """Вернуть множество возможных значения для указанной позиции
    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    col = get_col(grid, pos)
    row = get_row(grid, pos)
    block = get_block(grid, pos)
    # print(col)
    possible_values = set("123456789") - set(col) - set(row) - set(block)
    return possible_values
    pass


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла
    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    while True:
        pos = find_empty_positions(grid)
        if pos is None:
            return grid
        possible_values = find_possible_values(grid, pos)
        if len(possible_values) == 0:
            return None
        for value in possible_values:
            grid[pos[0]][pos[1]] = value
            sol = solve(grid)
            if sol is not None:
                return sol
            else:
                grid[pos[0]][pos[1]] = "."
        return None

    pass


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False
    >>> grid = read_sudoku('puzzle1.txt')
    >>> s=solve(grid)
    >>> check_solution(s)
    True

    >>> grid = read_sudoku('puzzle2.txt')
    >>> s=solve(grid)
    >>> check_solution(s)
    True

    >>> grid = read_sudoku('puzzle3.txt')
    >>> s=solve(grid)
    >>> check_solution(s)
    True

    >>> grid = read_sudoku('puzzle1.txt')
    >>> s=solve(grid)
    >>> s[0][0] = '1'
    >>> check_solution(s)
    False


    """
    # TODO: Add doctests with bad puzzles
    res = True
    for i in range(len(solution)):
        for j in range(len(solution[i])):
            test = []
            for k in range(len(solution)):
                test.append(solution[k].copy())
            test[i][j] = "."
            res = res and solution[i][j] in find_possible_values(test, [i, j])

    return res
    pass


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов
    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    # TODO: Implement the function to generate a Sudoku puzzle with N cells filled


    from random import randint, choice

    while True:
        points = []
        for i in range(9):
            for j in range(9):
                points.append((i, j))
        res = []
        count = 0
        grid = [['.' for _ in range(9)] for _ in range(9)]
        while count < N and count < 16:

            index=randint(0, len(points)-1)
            # print(index)
            i,j=points[index]

            if grid[i][j] == ".":
                if len(find_possible_values(grid, [i, j])) != 0:
                    grid[i][j] = choice(list(find_possible_values(grid, [i, j])))
                    count += 1
                    points.pop(index)
                else:
                    break
        for i in range(len(grid)):
            res.append(grid[i].copy())
        solution = solve(grid)

        if solution is not None:
            points = []
            for i in range(9):
                for j in range(9):
                    points.append((i, j))
            for i in range(81-(N if N<81 else 81)):
                index = randint(0, len(points) - 1)
                # print(index)
                i, j = points[index]
                if solution[i][j] != ".":
                    solution[i][j] = "."
                    points.pop(index)
            return solution



if __name__ == "__main__":
    # for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
    #     grid = read_sudoku(fname)
    #     display(grid)
    #     solution = solve(grid)
    #     if not solution:
    #         print(f"Puzzle {fname} can't be solved")
    #     else:
    #         display(solution)

    # generate_sudoku(40)
    grid = generate_sudoku(40)
    expected_unknown = 41
    actual_unknown = sum(1 for row in grid for e in row if e == ".")
    print(actual_unknown)
    # self.assertEqual(expected_unknown, actual_unknown)
    print(1)
    solution = solve(grid)
    solved = check_solution(solution)
    print(solved)
    # self.assertTrue(solved)
    print(2)
    grid = generate_sudoku(1000)
    expected_unknown = 0
    actual_unknown = sum(1 for row in grid for e in row if e == ".")
    # self.assertEqual(expected_unknown, actual_unknown)
    print(actual_unknown)
    print(3)
    solution = solve(grid)
    solved = check_solution(solution)
    # self.assertTrue(solved)
    print(4)

    grid = generate_sudoku(0)
    expected_unknown = 81
    actual_unknown = sum(1 for row in grid for e in row if e == ".")
    # self.assertEqual(expected_unknown, actual_unknown)
    print(actual_unknown)
    print(5)
    solution = solve(grid)
    solved = check_solution(solution)
    print(solved)
    # self.assertTrue(solved)
