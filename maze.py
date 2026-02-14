import random
from config_validation import ErrorInConfigFile


class Maze:
    direction = {
    "N" : (0, -1, "N", "S"),
    "S" : (0, +1, "S", "N"),
    "W" : (-1, 0, "W", "E"),
    "E" : (+1, 0, "E", "W"),
    }
    def __init__(self, data: dict):
        self.width = data["WIDTH"]
        self.height = data["HEIGHT"]
        self.entry = data["ENTRY"]
        self.exit = data["EXIT"]
        self.cell_size = self.calc_cell_size()
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

    def calc_cell_size(self) -> int:
        cell_size = 25
        while(cell_size*self.width >= 800):
            cell_size -= 1
            if(cell_size == 0):
                raise ErrorInConfigFile("cell_size <0")
        while(cell_size*self.height >= 800):
            cell_size -= 1
            if(cell_size == 0):
               raise ErrorInConfigFile("cell_size <0")
        return cell_size

    def my_42(self):
        w = int(self.width / 2)
        h = int(self.height / 2)
        i = 0
        while i < 8:
            self.cells[(h + 2) - i][w - 2].is_visited = True
            i += 1
        i = 0
        while i < 4:
            self.cells[h][(w - 3) - i].is_visited = True
            self.cells[(h - 2) + i][w - 4].is_visited = True
            i += 1
        self.cells[h - 1][w + 2].is_visited = True
        self.cells[h + 1][w].is_visited = True
        i = 0
        while i < 6:
            self.cells[h - 2][w + i].is_visited = True
            self.cells[h + 2][w + i].is_visited = True
            self.cells[h][w + i].is_visited = True
            i += 1  boli
    # def dsf_algorith(self, x, y):
    #     self.cells[y][x].is_visited = True
    #     directions = [(0, -1), (0, 1), (1, 0), (-1, 0)]
    #     random.shuffle(directions)
    #     i = 0
    #     while i < 4:
    #         dx, dy = directions[i]
    #         nx, ny = x + dx, y + dy
    #         if nx >= 0 and ny >= 0 and nx < self.width and ny < self.height:
    #             if self.cells[ny][nx].is_visited is False:
    #                 if dx == 0 and dy != 0:
    #                     if dy == 1:
    #                         self.cells[y][x].walls["S"] = False
    #                         self.cells[ny][nx].walls["N"] = False
    #                     if dy == -1:
    #                         self.cells[y][x].walls["N"] = False
    #                         self.cells[ny][nx].walls["S"] = False
    #                 else:
    #                     if dx == 1:
    #                         self.cells[y][x].walls["E"] = False
    #                         self.cells[ny][nx].walls["W"] = False
    #                     if dy == -1:
    #                         self.cells[y][x].walls["W"] = False
    #                         self.cells[ny][nx].walls["E"] = False
    #                 if self.dsf_algorith(nx, ny):
    #                     return True
    #         i += 1
    #     return False
    def dsf_algorith(self, x, y):
        """Iterative depth-first search to avoid recursion limit."""
        # Use a stack instead of recursion
        stack = [(x, y)]

        while stack:
            x, y = stack[-1]  # Peek at top of stack
            self.cells[y][x].is_visited = True

            # Get shuffled directions
            key = list(self.direction.keys())
            random.shuffle(key)

            # Try to find an unvisited neighbor
            found_unvisited = False

            for direction in key:
                n_x, n_y, d_dir, n_dir = self.direction[direction]
                m_x, m_y = x + n_x, y + n_y

                # Check bounds and if unvisited
                if 0 <= m_x < self.width and 0 <= m_y < self.height:
                    if not self.cells[m_y][m_x].is_visited:
                        # Remove walls
                        self.cells[y][x].walls[d_dir] = False
                        self.cells[m_y][m_x].walls[n_dir] = False

                        # Push new cell onto stack
                        stack.append((m_x, m_y))
                        found_unvisited = True
                        break  # Continue DFS from this neighbor

            # If no unvisited neighbors, backtrack
            if not found_unvisited:
                stack.pop()