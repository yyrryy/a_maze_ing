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


import os
from colorama import init
from maze_generator.parsing import read_file
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

color_index = 0
config = read_file()

width = config["WIDTH"]
height = config["HEIGHT"]
start = config["ENTRY"]
perfect = config["PERFECT"]
end = config["EXIT"]
seed = None
# try:
#     seed = config["SEED"]
# except Exception as e:
#     print("sds")
# print("++++++++++", seed)
maze = MazeGenerator(width, height, seed, perfect, start, end)

os.system("clear" if os.name != "nt" else "cls")
grid = maze.create_grid()
maze.generate_maze(grid)
maze.print_maze(grid, start, end, [], COLORS[color_index])
path = []
show_path = False
while True:
    print(f"Current maze seed: {maze.seed}")
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
            os.system("clear" if os.name != "nt" else "cls")
            show_path = False
            grid = maze.create_grid()
            maze.generate_maze(grid)
            maze.print_maze(grid, start, end, [], COLORS[color_index])
        elif choice == 2:
            os.system("clear" if os.name != "nt" else "cls")
            show_path = not show_path
            if show_path:
                path = maze.solve_maze(grid)
            else:
                path = []
            maze.print_maze(grid, start, end, path, COLORS[color_index])
            #print(maze.solve_maze(grid))

        elif choice == 3:
            os.system("clear" if os.name != "nt" else "cls")
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
