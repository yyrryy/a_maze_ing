class cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.isvisited = False
        self.walls = {"W": True, "S": True, "N": True, "E": True}


def create_grid(width, height):
    result = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append(cell(x, y))
        result.append(row)
    return result


# ===============================
# 🔵 رسم 42 في منتصف المتاهة
# ===============================
def draw_42(grid):
    height = len(grid)
    width = len(grid[0])

    pattern = [
        "🟦   🟦🟦🟦 ",
        "🟦   🟦   🟦",
        "🟦🟦🟦 🟦🟦🟦 ",
        "    🟦      ",
        "    🟦      ",
        "    🟦      ",
        "    🟦      "
    ]

    pattern_height = len(pattern)
    pattern_width = len(pattern[0])

    start_y = (height - pattern_height) // 2
    start_x = (width - pattern_width) // 2

    for y in range(pattern_height):
        for x in range(pattern_width):
            if pattern[y][x] == "🟦":
                grid[start_y + y][start_x + x].isvisited = True


# ===============================
# 🖨️ طباعة المتاهة
# ===============================
def print_maze_with_start_gift(grid, entry, exit):
    height = len(grid)
    width = len(grid[0])
    ex, ey = exit
    sx, sy = entry

    for y in range(height):

        # --- Top walls ---
        top_line = "+"
        for x in range(width):
            top_line += "----+" if grid[y][x].walls["N"] else "    +"
        print(top_line)

        # --- Middle cells ---
        middle_line = ""
        for x in range(width):

            middle_line += "|" if grid[y][x].walls["W"] else " "

            if (x, y) == (sx, sy):
                middle_line += " 🚶 "
            elif (x, y) == (ex, ey):
                middle_line += " 🎁 "
            elif grid[y][x].isvisited:
                middle_line += " 🟦 "
            else:
                middle_line += "    "

        middle_line += "|" if grid[y][width - 1].walls["E"] else " "
        print(middle_line)

    # --- Bottom border ---
    bottom_line = "+"
    for x in range(width):
        bottom_line += "----+" if grid[height - 1][x].walls["S"] else "    +"
    print(bottom_line)


# ===============================
# 🧮 تحويل الجدران إلى Hex
# ===============================
def get_hexa(c: cell):
    res = 0
    if c.walls["N"]:
        res |= 1
    if c.walls["E"]:
        res |= 2
    if c.walls["S"]:
        res |= 4
    if c.walls["W"]:
        res |= 8
    return format(res, 'X')


# ===============================
# 💾 كتابة المتاهة إلى ملف
# ===============================
def write_to_file(grid, filename="maze.txt"):
    height = len(grid)
    width = len(grid[0])

    with open(filename, "w") as f:
        for y in range(height):
            for x in range(width):
                f.write(get_hexa(grid[y][x]))
            f.write("\n")


# ===============================
# 🚀 التشغيل
# ===============================
WIDTH = 20
HEIGHT = 15

grid = create_grid(WIDTH, HEIGHT)

ENTRY = (3, 4)
EXIT = (19, 14)

draw_42(grid)

print_maze_with_start_gift(grid, ENTRY, EXIT)

# write_to_file(grid)