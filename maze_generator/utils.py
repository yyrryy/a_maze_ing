from typing import List, Optional, Tuple
from collections import deque


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
        #((maze_width // 2) - 2, (maze_height // 2) + 1),
        ((maze_width // 2) - 1, (maze_height // 2)),
        ((maze_width // 2) - 1, (maze_height // 2) + 1),
        ((maze_width // 2) - 1, (maze_height // 2) + 2)
    ]
    
    return cells


def reset_cells(grid, width, height):
    cells_42 = _42cells(width, height)
    #print(grid)
    for cells in grid:
        for cell in cells:
            x, y = cell.x, cell.y
            cell.isvisited = False
            cell.is42 = False
            if (x, y) in cells_42:
                cell.isvisited = True
                cell.is42 = True




def get_neighbors(grid, current_cell, width, height):
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

def get_open_neighbors(grid, current_cell, width, height):
    neighbors = []
    this_cell_x = current_cell.x
    this_cell_y = current_cell.y
    this_cell = grid[current_cell.x][current_cell.y]
    #print("getting open neigbors of", this_cell_x, this_cell_y)

    directions = [
        ("N", 0, -1),
        ("S", 0, 1),
        ("E", 1, 0),
        ("W", -1, 0),
    ]

    for direction, x, y in directions:
        if 0 <= current_cell.x < width and 0 <= current_cell.y < height:
            #print("========from open walls=====", this_cell.isvisited, direction, this_cell.walls[direction])
            next_x = this_cell_x + x
            next_y = this_cell_y + y
            next_cell = grid[next_y][next_x]
            print("am in", this_cell_x, this_cell_y, "next cell", next_x, next_y, next_cell.isvisited, direction, this_cell.walls[direction], not next_cell.isvisited and not this_cell.walls[direction])
            if not next_cell.isvisited and not this_cell.walls[direction]:
                neighbors.append((next_x, next_y))
        current_cell.isvisited = True
    return neighbors

def get_path(path: dict, grid: list, color="\033[97m"):
    RESET = "\033[0m"
    solution_key=None
    for key, value in path.items():
        if value["is_solution"]:
            solution_key = key
    real_path = []


    current = solution_key

    while current is not None:
        real_path.append(current)
        current = path[current]["parent"]

    real_path.reverse()
    return real_path

def bfs_solver(maze, width, height, start, end):
    queue = deque([(start, [start])])  # (current_position, path)
    visited = {start}
    
    directions = [
        ("N", 0, -1),
        ("S", 0, 1),
        ("E", 1, 0),
        ("W", -1, 0),
    ]

    while queue:
        (x, y), path = queue.popleft()
        
        if (x, y) == end:
            return path  # Shortest path found
        
        for direcytion, dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (0 <= nx < width and 0 <= ny < height) and (maze[nx][ny] != '#' and (nx, ny) not in visited):
                new_path = path + [(nx, ny)]
                queue.append(((nx, ny), new_path))
                visited.add((nx, ny))
    
    return None

