class Token:
	def __init__(self, type, value=None):
		self.type = type
		self.value = value
		self.pos = []
	
	def set_pos(self, pos):
		self.pos = pos
		return self
	
	def __repr__(self) -> str:
		return f'({self.type}: {self.value})'