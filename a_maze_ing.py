import sys
import os
from time import sleep
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
        "\033[31m",  # Red
    ]

    def clear_screen():
        os.system("clear" if os.name != "nt" else "cls")

    color_index = 0

    def print_file(file_path, delay=0.05, color=COLORS[1]):
        clear_screen()
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                print(color + line.rstrip() + "\033[0m")
                sleep(delay)

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

    except (InvalideValue, ValueError) as e:
        print(e)
        sys.exit(1)

    print_file("paint_maze.txt", delay=0.03, color="\033[92m")

    clear_screen()
    print_file("paint_maze.txt", 0, "\033[92m")
    sleep(1.5)
    maze = MazeGenerator(width, height, seed, perfect, start, end,
                         output_file, fixed_seed_flag)
    # try:
    grid = maze.create_grid()
    maze.generate_maze(grid)
    maze.print_maze(grid, start, end, [], COLORS[color_index])
    maze.solve_maze(grid, True)
    path = []
    show_path = False
    while True:
        print("\n")
        print("═" * 40)
        print("║{:^38}║".format("A-Maze-ing"))
        print("╠" + "═" * 38 + "╣")
        print("║ {:<36} ║".format("1. Re-generate a new maze"))
        print("║ {:<36} ║".format("2. Show/Hide path from entry to exit"))
        print("║ {:<36} ║".format("3. Rotate maze colors"))
        print("║ {:<36} ║".format("4. Fix/Unfix seed"))
        print("║ {:<36} ║".format("5. Change Exit"))
        print("║ {:<36} ║".format("6. Quit"))
        print("╚" + "═" * 38 + "╝")

        try:
            choice = input("Choice? (1-6): ")
            try:
                choice = int(choice)
            except ValueError:
                print("Not valid input !")
                break

            if choice == 1:
                clear_screen()
                print_file("paint_maze.txt", 0, "\033[92m")
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
                maze = MazeGenerator(width, height, seed, perfect, start, end,
                                     output_file, fixed_seed_flag)
                # try:
                grid = maze.create_grid()
                maze.generate_maze(grid)
                maze.print_maze(grid, start, end, [], COLORS[color_index])
                maze.solve_maze(grid, True)
                path = []
                show_path = False
            elif choice == 2:
                clear_screen()
                print_file("paint_maze.txt", 0, "\033[94m")
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
                print_file("paint_maze.txt", 0, COLORS[color_index])
                print(f"Current maze seed: {maze.seed}")
                maze.print_maze(grid, start, end, path, COLORS[color_index])

            elif choice == 6:
                print("Goodbye 👋")
                print_file("exit.txt", delay=0.04, color="\033[31m")
                break
            elif choice == 4:
                fixed_seed_flag = not fixed_seed_flag
                maze.fix_seed()
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

                except (InvalideValue, ValueError) as e:
                    print(e)
                    sys.exit(1)
                maze = MazeGenerator(width, height, seed, perfect, start, end,
                                     output_file, fixed_seed_flag)
                # try:
                print_file("paint_maze.txt", 0, COLORS[color_index])
                grid = maze.create_grid()
                maze.generate_maze(grid)
                maze.print_maze(grid, start, end, [], COLORS[color_index])
                maze.solve_maze(grid, True)
                path = []
                show_path = False
            elif choice == 5:
                try:
                    show_path = False
                    width = maze.width
                    height = maze.height
                    coords = input("Enter exit coordinations [x,y]; ")
                    coords = coords.split(",")
                    try:
                        x, y = int(coords[0]), int(coords[1])
                    except Exception:
                        raise ValueError("please provide x,y coordinations")
                    if 0 < x > width or 0 < y > height:
                        print("coordinations are out of maze")
                    else:
                        try:
                            with open("config.txt", "w") as file:
                                print(f"""WIDTH={width}
HEIGHT={maze.height}
ENTRY={maze.start[0]},{maze.start[1]}
EXIT={x},{y}
perFect={maze.isperfect}
OUTPUT_FILE={maze.output_file}\n""",
                                    file=file)
                            if fixed_seed_flag:
                                with open("config.txt", "a") as file:
                                    print(f"SEED={maze.seed}", file=file)
                        except PermissionError:
                            print("No permission to open the config file")
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
                    maze = MazeGenerator(width, height, seed, perfect, start,
                                         end, output_file, fixed_seed_flag)
                    # try:
                    print_file("paint_maze.txt", 0, COLORS[color_index])
                    grid = maze.create_grid()
                    maze.generate_maze(grid)
                    maze.print_maze(grid, start, end, [], COLORS[color_index])
                    maze.solve_maze(grid, True)
                except (ValueError, KeyboardInterrupt) as e:
                    print("\nInput is not valid, Exiting", e)
                    break
                except Exception as e:
                    print("An unexpected error", e)
            else:
                print("Not valid input !")
                break
        except (KeyboardInterrupt, EOFError):
            break
except Exception as e:
    print(e)
