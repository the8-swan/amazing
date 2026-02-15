import random
from config_validation import ErrorInConfigFile


class Maze:
    direction = {
        "N": (0, -1, "N", "S"),
        "S": (0, +1, "S", "N"),
        "W": (-1, 0, "W", "E"),
        "E": (+1, 0, "E", "W"),
    }

    def __init__(self, data: dict):
        self.width = data["WIDTH"]
        self.height = data["HEIGHT"]
        self.entry = data["ENTRY"]
        self.exit = data["EXIT"]
        self.cell_size = self.calc_cell_size()
        self.wall_size = self.celc_wall_size()
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

    def celc_wall_size(self) -> int:
        if self.cell_size <= 10:
            return 1
        return 2

    def calc_cell_size(self) -> int:
        cell_size = 25
        while cell_size * self.width >= 800:
            cell_size -= 1
            if cell_size == 0:
                raise ErrorInConfigFile("cell_size <0")
        while cell_size * self.height >= 800:
            cell_size -= 1
            if cell_size == 0:
                raise ErrorInConfigFile("cell_size <0")
        return cell_size

    def my_42(self):
        cells = 1
        if self.cell_size <= 10:
            cells = 6
        w = int(self.width / 2)
        h = int((self.height / 2) - (cells / 2))
        for i in range(1, 4 * cells):
            for j in range(cells):
                self.cells[h + j][w - i].is_visited = "True"
                self.cells[h + j][w + i].is_visited = "True"
        for i in range(1, cells):
            for j in range(1, 4 * cells):
                self.cells[(h + cells) + j][w - i].is_visited = "True"
                self.cells[(h + cells) + j][w + i].is_visited = "True"

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

    def reset_maze(self):
        for row in self.cells:
            for cell in row:
                cell.is_visited = False
                cell.walls = {"S": True, "N": True, "W": True, "E": True}
