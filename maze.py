class Maze:
	def __init__(self, width, height, cell_size):
		self.width = width
		self.height = height
		self.cell_size = cell_size
		# cells[row][col]
		self.cells = self.create_cells(self.width, self.height)
	
	class Cell:
		def __init__(self, row, column):
			self.row = row
			self.column = column
			self.walls = {
				"left":True,
				"right":True,
				"top":True,
				"bottom":True
			}
			self.is_visited = False
			
	def create_cells(self, width, height):
		cells = []
		for col in range(height):
			row_data = []
			for row in range(width):
				row_data.append(self.Cell(row, col))
			cells.append(row_data)
		return cells

	def dsf_algorith(self):
		self.cells[0][0].
		direction = [(0, -1), (0, 1), (1, 0), (-1, 0)]

mymaze = Maze(20, 20, 30)
for col in range(20):
	for row in range(20):
		print(f"{row}",end=" ")
	print("")
# print(mymaze.cells)