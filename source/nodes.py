class Program:
	def __init__(self):
		self.body = []
	
	def push(self, value):
		self.body.append(value)
	
	def __repr__(self):
		return f"Program {self.body}"

class NumericLiteral:
	def __init__(self, value):
		self.value = value
	
	def __repr__(self):
		return f"NumericLiteral ({self.value})"

class StringLiteral:
	def __init__(self, value):
		self.value = value
	
	def __repr__(self):
		return f"StringLiteral ({self.value})"

class Literal:
	def __init__(self, value):
		self.value = value
	
	def __repr__(self):
		return f"Literal ({self.value})"

class BinaryExpr:
	def __init__(self, left, op, right):
		self.left = left
		self.op = op
		self.right = right
	
	def __repr__(self):
		return f"BinaryExpr ({self.left} {self.op} {self.right})"