# from cell import create_grid, cell
# from parsing import read_file
# from cell import print_maze


# config = read_file()
# width = config["WIDTH"]
# height = config["HEIGHT"]
# entry = config["ENTRY"]
# exit = config["EXIT"]

# grid = create_grid(width, height)


# print_maze(grid, entry, exit)

# print("\n\n")

# print("═" * 40)
# print("║{:^38}║".format("A-Maze-ing"))
# print("╠" + "═" * 38 + "╣")
# print("║ {:<36} ║".format("1. Re-generate a new maze"))
# print("║ {:<36} ║".format("2. Show/Hide path from entry to exit"))
# print("║ {:<36} ║".format("3. Rotate maze colors"))
# print("║ {:<36} ║".format("4. Quit"))
# print("╚" + "═" * 38 + "╝")
# choice = input("Choice? (1-4): ")
# import os
# def execute_choice(cc):
#     if int(cc)==3:
#         os.system("clear")
# execute_choice(choice)

import sys
import os
import time
from colorama import init
from maze_generator.parsing import read_file, InvalideValue
from maze_generator.maze_generator import MazeGenerator

init()  # Windows support

# ANSI Colors
COLORS = [
    "\033[97m",  # White
    "\033[92m",  # Green
    "\033[94m",  # Blue
    "\033[93m",  # Yellow
    "\033[95m",  # Magenta
    "\033[96m",  # Cyan
]
def clear_screen():
    os.system("clear" if os.name != "nt" else "cls")

color_index = 0
def print_title(file_path, delay=0.7, color=COLORS[1]):
    clear_screen()
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            print(color + line.rstrip() + "\033[0m")
            time.sleep(delay)
try:
    config = read_file()
    width = config["WIDTH"]
    height = config["HEIGHT"]
    start = config["ENTRY"]
    perfect = config["PERFECT"]
    end = config["EXIT"]
    try:
        seed = config["SEED"]
    except Exception:
        seed = None
except (InvalideValue, ValueError) as  e:
    print(e)
    sys.exit(1)

# try:
#     seed = config["SEED"]
# except Exception as e:
#     print("sds")
# print("++++++++++", seed)
#print_title("paint_maze.txt", delay=0.8, color=COLORS[color_index])

clear_screen()
maze = MazeGenerator(width, height, seed, perfect, start, end)
# try:
grid = maze.create_grid()
maze.generate_maze(grid)
maze.print_maze(grid, start, end, [], COLORS[color_index])
path = []
show_path = False
while True:
    
    # for cells in maze.grid:
    #     for cell in cells:
    #         print("====cells======", cell.walls, cell.isvisited)
    # maze.generate_maze(grid)
    # maze.print_maze(grid, entry, exit, COLORS[color_index])
    # for cells in maze.grid:
    #     for cell in cells:
    #         print(cell.x, cell.x, cell.isvisited, cell.is42)
    print("\n")
    print("═" * 40)
    print("║{:^38}║".format("A-Maze-ing"))
    print("╠" + "═" * 38 + "╣")
    print("║ {:<36} ║".format("1. Re-generate a new maze"))
    print("║ {:<36} ║".format("2. Show/Hide path from entry to exit"))
    print("║ {:<36} ║".format("3. Rotate maze colors"))
    print("║ {:<36} ║".format("4. Quit"))
    print("╚" + "═" * 38 + "╝")

    try:
        choice = input("Choice? (1-4): ")
        try:
            choice = int(choice)
        except ValueError:
            continue

        if choice == 1:
            clear_screen()
            show_path = False
            grid = maze.create_grid()
            maze.generate_maze(grid)
            maze.print_maze(grid, start, end, [], COLORS[color_index])
        elif choice == 2:
            clear_screen()
            show_path = not show_path
            if show_path:
                path = maze.solve_maze(grid)
            else:
                path = []
            maze.print_maze(grid, start, end, path, COLORS[color_index])
            #print(maze.solve_maze(grid))

        elif choice == 3:
            clear_screen()
            if show_path:
                path = maze.solve_maze(grid)
            else:
                path = []
            color_index = (color_index + 1) % len(COLORS)
            maze.print_maze(grid, start, end, path, COLORS[color_index])

        elif choice == 4:
            print("Goodbye 👋")
            break
        else:
            print("Not valid input !")
            break
    except (KeyboardInterrupt, EOFError):
        continue
# except Exception as e:
#     print(e) 