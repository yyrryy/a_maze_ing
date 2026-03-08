
# class cell:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#         self.isvisited = False
#         self.walls = {"W": True, "S": True, "N": True, "E": True}



# def create_grid(width, height):

#     row = []
#     result: list[list[cell]] = []


#     for y in range(height):
#         for x in range(width):
#             obj = cell(x, y)
#             row.append(obj)
#         result.append(row)
#         row = []
#     return result



# # def print_maze(grid):
# #     height = len(grid)
# #     width = len(grid[0])

# #     for y in range(height):

# #         # --- Print top walls of current row ---
# #         top_line = "+"
# #         for x in range(width):
# #             if grid[y][x].walls["N"]:
# #                 top_line += "----+"
# #             else:
# #                 top_line += "    +"
# #         print(top_line)

# #         # --- Print side walls of current row ---
# #         middle_line = ""
# #         for x in range(width):
# #             if grid[y][x].walls["W"]:
# #                 middle_line += "|"
# #             else:
# #                 middle_line += " "

# #             middle_line += "    "  # cell interior space

# #         # Last right wall of the row
# #         if grid[y][width - 1].walls["E"]:
# #             middle_line += "|"
# #         else:
# #             middle_line += " "

# #         print(middle_line)

# #     # --- Print bottom border ---
# #     bottom_line = "+"
# #     for x in range(width):
# #         if grid[height - 1][x].walls["S"]:
# #             bottom_line += "----+"
# #         else:
# #             bottom_line += "    +"
# #     print(bottom_line)









# def print_maze(grid: list[list[cell]], entry: tuple, exit: tuple):
#     height = len(grid)
#     width = len(grid[0])
#     ex, ey = exit
#     sx, sy = entry

#     # ===== Top Border =====
#     top_line = "┌"
#     for x in range(width):
#         if grid[0][x].walls["N"]:
#             top_line += "───"
#         else:
#             top_line += "   "

#         if x < width - 1:
#             top_line += "┬"
#     top_line += "┐"
#     print(top_line)

#     for y in range(height):

#         # ===== Middle Line (content + vertical walls) =====
#         middle_line = ""
#         for x in range(width):

#             # West wall
#             if x == 0:
#                 middle_line += "│" if grid[y][x].walls["W"] else " "
#             else:
#                 middle_line += "│" if grid[y][x].walls["W"] else " "

#             # Cell content
#             if (x, y) == (sx, sy):
#                 middle_line += " S "
#             elif (x, y) == (ex, ey):
#                 middle_line += " G "
#             else:
#                 middle_line += "   "

#         # East wall of last cell
#         middle_line += "│" if grid[y][width - 1].walls["E"] else " "
#         print(middle_line)

#         # ===== Bottom walls between rows =====
#         if y < height - 1:
#             separator = "├"
#             for x in range(width):
#                 if grid[y][x].walls["S"]:
#                     separator += "───"
#                 else:
#                     separator += "   "

#                 if x < width - 1:
#                     separator += "┼"
#             separator += "┤"
#             print(separator)

#     # ===== Final Bottom Border =====
#     bottom_line = "└"
#     for x in range(width):
#         if grid[height - 1][x].walls["S"]:
#             bottom_line += "───"
#         else:
#             bottom_line += "   "

#         if x < width - 1:
#             bottom_line += "┴"
#     bottom_line += "┘"
#     print(bottom_line)


# # def get_hexa(c: cell):

# #     res = 0

# #     if (c.walls["N"]):
# #         res |= 1
    
# #     if (c.walls["E"]):
# #         res |= 2
    
# #     if (c.walls["S"]):
# #         res |= 4
    
# #     if (c.walls["W"]):
# #         res |= 8
    
# #     return format(res, 'X')





# # def write_to_file(grid):

# #     height = len(grid)
# #     width = len(grid[0])

# #     for y in range(height):
# #         for x in range(width):
# #             print(get_hexa(grid[y][x]), end='')
# #         print()










# # grid = create_grid(10, 10)


# # # grid[1][1].walls = {"W": True, "S": True, "N": True, "E": False}
# # ENTRY = (3, 4)
# # EXIT = (9, 9)

# # print_maze(grid, ENTRY, EXIT)





# # write_to_file(grid)



#=======================================================






