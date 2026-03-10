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
            closed = self.walls[direction] is True
            value += closed << count
            count += 1
        return value
