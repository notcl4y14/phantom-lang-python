class BinaryExpr:
	def __init__(self, left, op, right):
		self.left = left
		self.op = op
		self.right = right
	
	def __repr__(self):
		return f"BinaryExpr ({self.left} {self.op} {self.right})"