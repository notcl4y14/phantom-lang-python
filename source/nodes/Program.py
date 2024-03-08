class Program:
	def __init__(self):
		self.body = []
	
	def push(self, value):
		self.body.append(value)
	
	def __repr__(self):
		return f"Program {self.body}"