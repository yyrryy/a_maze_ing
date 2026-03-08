import random
from typing import List, Optional, Tuple
from .utils import _42cells, get_neighbors, reset_cells, get_path, print_hexa
from collections import deque
from time import sleep
import sys
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.isvisited = False
        self.is42 = False
        self.walls = {"N": True, "E": True, "S": True, "W": True}
    
    def remove_walls(self, neighbor, direction):
        if direction == "N":
            self.walls["N"] = False
            neighbor.walls["S"] = False
        elif direction == "S":
            self.walls["S"] = False
            neighbor.walls["N"] = False
        elif direction == "E":
            self.walls["E"] = False
            neighbor.walls["W"] = False
        elif direction == "W":
            self.walls["W"] = False
            neighbor.walls["E"] = False

    def get_value(self) -> int:
        value = 0
        count = 0
        for direction in self.walls:
            closed = (self.walls[direction] is True)
            value += closed << count
            count += 1
        return value


class MazeGenerator:
    def __init__(self, width: int, height: int,
                 seed: int | None, isperfect: bool, start: tuple, end: tuple, output_file: str, fixed_seed) -> None:
        self.start = start
        self.end = end
        self.width = width
        self.height = height
        self.grid: List[List[Cell]] = self.create_grid()
        self.isperfect = isperfect
        self.output_file = output_file
        self.fixed_seed = fixed_seed
        #self.bonuses: List = []
        if seed is not None:
            self.seed = seed
        else:
            self.seed = random.randint(0, 10**6)
        # if seed is None:
        #     seed = random.randint(0, 10**6)
        #self.seed = seed

        # Create a dedicated RNG
        self.rng = random.Random(self.seed)
        # if seed:
        #     self.seed = seed
        # else:
        #     self.seed = random.randint(0, 10**6)

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
    

    
    # dfs generating maze
    def generate_maze(self, grid):
        height = len(grid)
        width = len(grid[0])
        #print("===========", height, width)
        stack = []

        #random.seed(self.seed)
        
        
        start = grid[0][0]
        start.isvisited = True
        stack.append(start)
        
        random.seed(str(self.seed))
        print(f"Current maze seed: {self.seed}")
        while stack:
            current_cell = stack[-1]
            neighbors = get_neighbors(grid, current_cell, width, height)
            #random.seed(this_seed)
            if neighbors:
                # direction, next_cell = random.choice(neighbors)
                direction, next_cell = random.choice(neighbors)
                
                current_cell.remove_walls(next_cell, direction)

                next_cell.isvisited = True
                stack.append(next_cell)
            else:
                stack.pop()
        # directions = [
        #     ("N", 0, -1),
        #     ("S", 0, 1),
        #     ("E", 1, 0),
        #     ("W", -1, 0),
        # ]
        # if not self.isperfect:
        #     extra_walls_to_break = int((self.width * self.height) / 10)
        #     for _ in range(extra_walls_to_break):
        #         rx, ry = random.randint(1, self.width-1), \
        #             random.randint(1, self.height-1)
        #         random_dir = random.choice(directions)
        #         direction, dx, dy = random_dir
        #         nx, ny = rx + dx, ry + dy
        #         # to make sure if it's owned by 42 block
        #         curent_cell = self.get_cell(rx, ry)
        #         next_cell = self.get_cell(nx, ny)
        #         if curent_cell and next_cell:
        #             if self.inside_grid(nx, ny) and not curent_cell.is42 and\
        #                     not next_cell.is42:
        #                 pass
        #                 # current_cell.remove_walls(next_cell, direction)
        #                 # self.carve(rx, ry, nx, ny, random_dir)
        reset_cells(grid, width, height)
        
        print_hexa(self.output_file, grid, self.start, self.end)

    # solve using BFS
    def solve_maze(self, grid, print_to_file):
        # print("asdasd")
        start = self.start
        goal = self.end

        cells_to_explore = [start]
        visited = set([start])
        parents = {
            start: {
                "parent": None,
                "is_solution": False,
                "direction": None
            }
        }

        while cells_to_explore:
            x, y = cells_to_explore.pop(0)

            if (x, y) == goal:
                parents[(x, y)]["is_solution"] = True
                break

            cell = grid[y][x]
            directions = {
                ('N', 0, -1),
                ('S', 0, 1),
                ('E', 1, 0),
                ('W', -1, 0),
            }
            #print("cell", cell, cell.walls["N"], cell.walls["S"], cell.walls["W"], cell.walls["E"])
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
                        "direction": direction
                    }
                    cells_to_explore.append((nx, ny))
        return get_path(parents, grid, self.output_file, print_to_file)
        #return parents

    def print_maze(self, grid, entry, end, path, color="\033[97m"):
        RESET = "\033[0m"
        height = len(grid)
        width = len(grid[0])
        ex, ey = end
        sx, sy = entry
        cells_of_42 = _42cells(width, height)
        if (entry in cells_of_42 or end in cells_of_42):
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
                    #print(this_cell.is42)
                    middle_line += " ▣ "
                elif (x, y) in path:
                    middle_line += f" * "
                else:
                    #middle_line += f"{x},{y}"
                    middle_line += f"   "
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
