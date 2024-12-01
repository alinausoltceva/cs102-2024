import pathlib
import typing as tp
import random

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
    group=[[0] * n for i in range(len(values)//n)]
    print(group)
    for i in range (len(values)//n):
        group[i]=values[n*(i):n*(i+1)]
    return group

def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    return grid[pos[0]]

def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    col=[]
    for i in range (3):
        col.append(grid[i][pos[1]])
    return col

def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    block=grid[3*(pos[0]//3):3*(pos[0]//3)+3]
    block=[i[3*(pos[1]//3):3*(pos[1]//3)+3] for i in block]
    answ=[]
    for i in range(len(block)):
        answ+=block[i]
    return answ

def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j]=='.':
                a=(i, j)
                return a

def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    values = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    possible_in_row=[i for i in values if i not in get_row(grid, pos)]
    possible_in_col=[i for i in values if i not in get_col(grid, pos)]
    possible_in_block=[i for i in values if i not in get_block(grid, pos)]
    anws=[i for i in values if i in possible_in_row and i in possible_in_col and i\
          in possible_in_block]
    return possible_in_row, possible_in_col, possible_in_block, set(anws)

def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    dots = sum(row.count('.') for row in grid)
    if dots == 81:
        return generate_sudoku(81)
    empty = find_empty_positions(grid)
    if not empty:
        return grid
    values = find_possible_values(grid, empty)
    answ = []
    for x in values:
        new_grid = [row[:] for row in grid]
        new_grid[empty[0]][empty[1]] = x
        result = solve(new_grid)
        if result:
            answ.append(result)
    if not answ:
        return None
    return max(answ, key=lambda x: check_solution(x) + len(x))

def check_solution(grid: tp.List[tp.List[str]]) -> bool:
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            row = get_row(grid, [i, j])
            col = get_col(grid, [i, j])
            block = get_block(grid, [i, j])
            if len(row)==len(sorted(set(row))) and\
                    len(col)==len(sorted(set(col))) and\
                    len(block)==len(sorted(set(block))):
                return True
    else:
        return False

def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    grid = [['.' for i in range(9)] for j in range(9)]
    N = max(0, min(N, 81))
    positions = [(row, col) for row in range(9) for col in range(9)]
    random.shuffle(positions)
    for i in range(81 - N):
        row, col = positions[i]
        grid[row][col] = '.'
    return grid

if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)