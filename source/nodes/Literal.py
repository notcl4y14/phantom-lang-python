class Literal:
	def __init__(self, value):
		self.value = value
	
	def __repr__(self):
		return f"Literal ({self.value})"