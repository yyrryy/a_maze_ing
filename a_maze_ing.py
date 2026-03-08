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
from mazegen import MazeGenerator, read_file, InvalideValue
try:
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
    fixed_seed_flag = False
    try:
        config = read_file()
        width = config["WIDTH"]
        height = config["HEIGHT"]
        start = config["ENTRY"]
        perfect = config["PERFECT"]
        end = config["EXIT"]
        output_file = config["OUTPUT_FILE"]
        try:
            seed = config["SEED"]
            fixed_seed_flag = True
        except Exception:
            seed = None

    except (InvalideValue, ValueError) as  e:
        print(e)
        sys.exit(1)

    #print_title("paint_maze.txt", delay=0.8, color=COLORS[color_index])

    clear_screen()
    maze = MazeGenerator(width, height, seed, perfect, start, end, output_file, fixed_seed_flag)
    # try:
    grid = maze.create_grid()
    maze.generate_maze(grid)
    maze.print_maze(grid, start, end, [], COLORS[color_index])
    maze.solve_maze(grid, True)
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
        print("║ {:<36} ║".format("5. Fix/Unfix seed"))
        print("║ {:<36} ║".format("6. Change Exit"))
        print("╚" + "═" * 38 + "╝")

        try:
            choice = input("Choice? (1-6): ")
            try:
                choice = int(choice)
            except ValueError:
                continue

            if choice == 1:
                clear_screen()
                try:
                    config = read_file()
                    width = config["WIDTH"]
                    height = config["HEIGHT"]
                    start = config["ENTRY"]
                    perfect = config["PERFECT"]
                    end = config["EXIT"]
                    output_file = config["OUTPUT_FILE"]
                    try:
                        seed = config["SEED"]
                    except Exception:
                        seed = None

                except (InvalideValue, ValueError) as  e:
                    print(e)
                    sys.exit(1)
                clear_screen()
                maze = MazeGenerator(width, height, seed, perfect, start, end, output_file, fixed_seed_flag)
                # try:
                grid = maze.create_grid()
                maze.generate_maze(grid)
                maze.print_maze(grid, start, end, [], COLORS[color_index])
                maze.solve_maze(grid, True)
                path = []
                show_path = False
            elif choice == 2:
                clear_screen()
                
                show_path = not show_path
                if show_path:
                    path = maze.solve_maze(grid, False)
                else:
                    path = []
                print(f"Current maze seed: {maze.seed}")
                maze.print_maze(grid, start, end, path, COLORS[color_index])

            elif choice == 3:
                clear_screen()
                if show_path:
                    path = maze.solve_maze(grid, False)
                else:
                    path = []
                color_index = (color_index + 1) % len(COLORS)
                print(f"Current maze seed: {maze.seed}")
                maze.print_maze(grid, start, end, path, COLORS[color_index])

            elif choice == 4:
                print("Goodbye 👋")
                break
            elif choice == 5:
                fixed_seed_flag = not fixed_seed_flag
                maze.fix_seed()
                continue
            elif choice == 6:
                try:
                    show_path = not show_path
                    width = maze.width
                    height = maze.height
                    coords = input("Enter exit coordinations [x,y]; ")
                    coords = coords.split(",")
                    x, y = int(coords[0]), int(coords[1])
                    with open("config.txt", "w") as file:
                        print(f"""WIDTH={width}
ENTRY={maze.start[0]},{maze.start[1]}
EXIT={x},{y}
perFect={maze.isperfect}
HEIGHT={maze.height}
OUTPUT_FILE={maze.output_file}
""", file=file)
                    if fixed_seed_flag:
                        with open("config.txt", "a") as file:
                            print(f"SEED={maze.seed}", file=file)
                    try:
                        config = read_file()
                        width = config["WIDTH"]
                        height = config["HEIGHT"]
                        start = config["ENTRY"]
                        perfect = config["PERFECT"]
                        end = config["EXIT"]
                        output_file = config["OUTPUT_FILE"]
                        try:
                            seed = config["SEED"]
                        except Exception:
                            seed = None

                    except (InvalideValue, ValueError) as e:
                        print(e)
                        sys.exit(1)
                    clear_screen()
                    maze = MazeGenerator(width, height, seed, perfect, start, end, output_file, fixed_seed_flag)
                    # try:
                    grid = maze.create_grid()
                    maze.generate_maze(grid)
                    maze.print_maze(grid, start, end, [], COLORS[color_index])
                    maze.solve_maze(grid, True)
                except (ValueError, KeyboardInterrupt) as e:
                    print("\nInput not valid, Exiting", e)
                    break
                except Exception as e:
                    print("An unexpected error", e)
            else:
                print("Not valid input !")
                break
        except (KeyboardInterrupt, EOFError):
            continue
except Exception as e:
    print(e)