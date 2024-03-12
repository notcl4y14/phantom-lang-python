class Error:
	def __init__(self, details, pos):
		self.details = details
		self.pos = pos
	
	def __repr__(self):
		filename = self.pos[0].filename
		details = self.details

		line = self.pos[0].line + 1

		if self.pos[0].line != self.pos[1].line:
			line = f"{self.pos[0].line + 1}-{self.pos[1].line + 1}"
			
		column = self.pos[0].column + 1

		if self.pos[0].column != self.pos[1].column:
			column = f"{self.pos[0].column + 1}-{self.pos[1].column + 1}"
		
		return f"{filename}: {line} : {column} : {details}"