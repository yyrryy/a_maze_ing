import random
from typing import List, Tuple, Optional
from .utils import _42cells, get_neighbors, reset_cells, get_path, print_hexa
from time import sleep
import sys
from .cell import Cell


class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        isperfect: bool,
        start: Tuple,
        end: Tuple,
        output_file: str,
        fixed_seed: bool,
        seed: Optional[int] = None,
    ) -> None:
        self.start = start
        self.end = end
        self.width = width
        self.height = height
        self.grid: List[List[Cell]] = self.create_grid()
        self.isperfect = isperfect
        self.output_file = output_file
        self.fixed_seed = fixed_seed
        if seed is not None:
            self.seed = seed
        else:
            self.seed = random.randint(0, 10**6)

    def fix_seed(self):
        try:
            if self.fixed_seed:
                print("SEED unfixed, choose again")
            else:
                print("SEED fixed, choose again")
            if self.fixed_seed:
                with open("config.txt", "r") as f:
                    lines = f.readlines()
                not_in_file = False
                for i in range(len(lines)):
                    if lines[i].lower().startswith("seed="):
                        lines[i] = ""
                with open("config.txt", "w") as f:
                    f.writelines(lines)
                self.fixed_seed = False
            else:
                with open("config.txt", "r") as f:
                    lines = f.readlines()
                not_in_file = False
                for i in range(len(lines)):
                    if lines[i].lower().startswith("seed="):
                        lines[i] = f"\nseed={self.seed}\n"
                    else:
                        not_in_file = True
                with open("config.txt", "w") as f:
                    f.writelines(lines)
                    if not_in_file:
                        if lines and lines[-1].endswith("\n"):
                            f.write(f"seed={self.seed}\n")
                        else:
                            f.write(f"\nseed={self.seed}\n")
                self.fixed_seed = True
        except Exception as e:
            print(f"ERROR: {e}")

    def create_grid(self):
        result = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                cell = Cell(x, y)
                if (x, y) in _42cells(self.width, self.height):
                    cell.isvisited = True
                    cell.is42 = True
                row.append(cell)
            result.append(row)
        return result

    def inside_grid(self, x: int, y: int) -> bool:
        if 0 <= x < self.width and 0 <= y < self.height:
            return True
        return False

    def get_cell(self, x: int, y: int) -> Cell | None:
        if not self.inside_grid(x, y):
            return None
        return self.grid[y][x]

    def generate_maze(self, grid):
        height = len(grid)
        width = len(grid[0])

        stack = []

        start = grid[0][0]
        start.isvisited = True
        stack.append(start)

        random.seed(str(self.seed))
        print(f"Current maze seed: {self.seed}")
        while stack:
            current_cell = stack[-1]
            neighbors = get_neighbors(grid, current_cell, width, height)

            if neighbors:
                direction, next_cell = random.choice(neighbors)

                current_cell.remove_walls(next_cell, direction)

                next_cell.isvisited = True
                stack.append(next_cell)
            else:
                stack.pop()

        reset_cells(grid, width, height)

        print_hexa(self.output_file, grid, self.start, self.end)

    # solve using BFS
    def solve_maze(self, grid, print_to_file):
        start = self.start
        goal = self.end

        cells_to_explore = [start]
        visited = set([start])
        parents = {start: {
            "parent": None, "is_solution": False, "direction": None}
            }

        while cells_to_explore:
            x, y = cells_to_explore.pop(0)

            if (x, y) == goal:
                parents[(x, y)]["is_solution"] = True
                break

            cell = grid[y][x]
            directions = {
                ("N", 0, -1),
                ("S", 0, 1),
                ("E", 1, 0),
                ("W", -1, 0),
            }
            for direction, dx, dy in directions:

                if cell and cell.walls[direction]:
                    continue

                nx, ny = x + dx, y + dy

                if not self.inside_grid(nx, ny):
                    continue

                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parents[(nx, ny)] = {
                        "parent": (x, y),
                        "is_solution": False,
                        "direction": direction,
                    }
                    cells_to_explore.append((nx, ny))
        return get_path(parents, grid, self.output_file, print_to_file)

    def print_maze(self, grid, entry, end, path, color="\033[97m"):
        RESET = "\033[0m"
        height = len(grid)
        width = len(grid[0])
        ex, ey = end
        sx, sy = entry
        cells_of_42 = _42cells(width, height)
        if entry in cells_of_42 or end in cells_of_42:
            print("entry or exit shouldnt be in 42 cells")
            sys.exit(1)

        # ===== Top Border =====
        top_line = "┌"
        for x in range(width):
            top_line += "───" if grid[0][x].walls["N"] else "   "
            if x < width - 1:
                top_line += "o"
        top_line += "┐"
        print(color + top_line + RESET)

        for y in range(height):

            middle_line = ""
            for x in range(width):

                middle_line += "│" if grid[y][x].walls["W"] else " "

                if (x, y) == (sx, sy):
                    middle_line += " S "
                elif (x, y) == (ex, ey):
                    middle_line += " E "
                elif (x, y) in cells_of_42:
                    this_cell = self.get_cell(x, y)
                    this_cell.is42 = True
                    this_cell.isvisited = True
                    middle_line += "\033[102m   \033[0m" + color
                elif (x, y) in path:
                    middle_line += " * "
                else:
                    middle_line += "   "
                sleep(0.003)

            middle_line += "│" if grid[y][width - 1].walls["E"] else " "
            print(color + middle_line + RESET)

            if y < height - 1:
                separator = "├"
                for x in range(width):
                    separator += "───" if grid[y][x].walls["S"] else "   "
                    if x < width - 1:
                        separator += "o"
                separator += "┤"
                print(color + separator + RESET)

        bottom_line = "└"
        for x in range(width):
            bottom_line += "───" if grid[height - 1][x].walls["S"] else "   "
            if x < width - 1:
                bottom_line += "o"
        bottom_line += "┘"
        print(color + bottom_line + RESET)
