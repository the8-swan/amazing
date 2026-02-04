import random


class Maze:
    def __init__(self, data: dict):
        self.width = data["WIDTH"]
        self.height = data["HEIGHT"]
        self.entry = data["ENTRY"]
        self.exit = data["EXIT"]
        self.cell_size = 30
        # cells[row][col]
        self.cells = self.create_cells(self.width, self.height)

    class Cell:
        def __init__(self, row, column):
            self.row = row
            self.column = column
            self.walls = {"S": True, "N": True, "W": True, "E": True}
            self.is_visited = False

    def create_cells(self, width, height):
        cells = []
        for col in range(height):
            row_data = []
            for row in range(width):
                row_data.append(self.Cell(row, col))
            cells.append(row_data)
        return cells

    def dsf_algorith(self, x, y):
        self.cells[y][x].is_visited = True
        directions = [(0, -1), (0, 1), (1, 0), (-1, 0)]
        random.shuffle(directions)
        i = 0
        while i < 4:
            dx, dy = directions[i]
            nx, ny = x + dx, y + dy
            if nx >= 0 and ny >= 0 and nx < self.width and ny < self.height:
                if self.cells[ny][nx].is_visited is False:
                    if dx == 0 and dy != 0:
                        if dy == 1:
                            self.cells[y][x].walls["S"] = False
                            self.cells[ny][nx].walls["N"] = False
                        if dy == -1:
                            self.cells[y][x].walls["N"] = False
                            self.cells[ny][nx].walls["S"] = False
                    else:
                        if dx == 1:
                            self.cells[y][x].walls["E"] = False
                            self.cells[ny][nx].walls["W"] = False
                        if dy == -1:
                            self.cells[y][x].walls["W"] = False
                            self.cells[ny][nx].walls["E"] = False
                    if self.dsf_algorith(nx, ny):
                        return True
            i += 1
        return False
