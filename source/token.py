class Token:
	def __init__(self, type, value):
		self.type = type
		self.value = value
	
	def __repr__(self) -> str:
		return f'({self.type}: {self.value})'