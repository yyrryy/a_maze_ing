from typing import List, Tuple
from .cell import Cell


def _42cells(
        maze_width: int,
        maze_height: int
                        ) -> List[Tuple]:
    cells = [
        ((maze_width // 2) + 2, (maze_height // 2) - 2),
        ((maze_width // 2) + 1, (maze_height // 2) - 2),
        ((maze_width // 2) + 3, (maze_height // 2) - 2),
        ((maze_width // 2) + 3, (maze_height // 2) - 1),
        ((maze_width // 2) + 3, (maze_height // 2)),
        ((maze_width // 2) + 2, (maze_height // 2)),
        ((maze_width // 2) + 1, (maze_height // 2)),
        ((maze_width // 2) + 1, (maze_height // 2) + 1),
        ((maze_width // 2) + 1, (maze_height // 2) + 2),
        ((maze_width // 2) + 2, (maze_height // 2) + 2),
        ((maze_width // 2) + 3, (maze_height // 2) + 2),
        \
        ((maze_width // 2) - 3, (maze_height // 2) - 2),
        ((maze_width // 2) - 3, (maze_height // 2) - 1),
        ((maze_width // 2) - 3, (maze_height // 2)),
        ((maze_width // 2) - 2, (maze_height // 2)),
        ((maze_width // 2) - 1, (maze_height // 2)),
        ((maze_width // 2) - 1, (maze_height // 2) + 1),
        ((maze_width // 2) - 1, (maze_height // 2) + 2)
    ]
    return cells


def reset_cells(grid: List[List[Cell]], width: int, height: int) -> None:
    cells_42 = _42cells(width, height)
    for cells_in_grid in grid:
        for cell in cells_in_grid:
            x, y = cell.x, cell.y
            cell.isvisited = False
            cell.is42 = False
            if (x, y) in cells_42:
                cell.isvisited = True
                cell.is42 = True


def get_neighbors(grid: List[List[Cell]], current_cell: Cell,
                  width: int, height: int) -> List[Tuple[str, Cell]]:
    neighbors = []

    this_cell_x = current_cell.x
    this_cell_y = current_cell.y

    directions = [
        ("N", 0, -1),
        ("S", 0, 1),
        ("E", 1, 0),
        ("W", -1, 0),
    ]

    for direction, x, y in directions:
        next_x = this_cell_x + x
        next_y = this_cell_y + y

        if 0 <= next_x < width and 0 <= next_y < height:
            neighbor = grid[next_y][next_x]
            if not neighbor.isvisited:
                neighbors.append((direction, neighbor))
    return neighbors


def get_path(path: dict, grid: list, output_file: str,
             print_to_file: bool, color="\033[97m"):
    # RESET = "\033[0m"
    solution_key = None
    for key, value in path.items():
        if value["is_solution"]:
            solution_key = key
    real_path = []
    real_direction = []
    current = solution_key
    current_direction = path[solution_key]["direction"]
    while current is not None:
        real_path.append(current)
        if current_direction:
            real_direction.append(current_direction)
            current_direction = path[current]["direction"]
        current = path[current]["parent"]
    if print_to_file:
        with open(output_file, "a") as f:
            real_direction.reverse()
            print(*real_direction, sep="", file=f)
    real_path.reverse()
    return real_path


def print_hexa(output_file: str, grid: List[List[Cell]], start: Tuple,
               end: Tuple) -> None:
    with open(output_file, "w") as f:
        for cells in grid:
            for cell in cells:
                value = cell.get_value()
                f.write(f"{value:X}")  # Direct hex formatting
            f.write("\n")
        f.write("\n")
        f.write(f"{start[0]},{start[1]}")
        f.write("\n")
        f.write(f"{end[0]},{end[1]}")
        f.write("\n")
