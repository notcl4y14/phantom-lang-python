class Position:
	def __init__(self, filename, index, line, column):
		self.filename = filename
		self.index = index
		self.line = line
		self.column = column
	
	def advance(self, char = "", delta = 1):
		self.index += delta
		self.column += delta

		if char == "\n":
			self.column = 0
			self.line += 1
		
		return self
	
	def clone(self):
		return Position(self.filename, self.index, self.line, self.column)