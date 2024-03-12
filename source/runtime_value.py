class RuntimeValue:
	def __init__(self, type, value):
		self.type = type
		self.value = value
	
	def __repr__(self):
		return str(self.type) + ": " + str(self.value)