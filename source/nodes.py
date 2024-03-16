class Node:
	def __init__(self):
		self.pos = []

	def set_pos(self, pos):
		self.pos = pos
		return self

class Program(Node):
	def __init__(self):
		super()
		self.body = []
	
	def push(self, value):
		self.body.append(value)
	
	def __repr__(self):
		return f"Program {self.body}"

class NumericLiteral(Node):
	def __init__(self, value):
		super()
		self.value = value
	
	def __repr__(self):
		return f"NumericLiteral ({self.value})"

class StringLiteral(Node):
	def __init__(self, value):
		super()
		self.value = value
	
	def __repr__(self):
		return f"StringLiteral ({self.value})"

class Literal(Node):
	def __init__(self, value):
		super()
		self.value = value
	
	def __repr__(self):
		return f"Literal ({self.value})"

class Identifier(Node):
	def __init__(self, value):
		super()
		self.value = value
	
	def __repr__(self):
		return f"Identifier ({self.value})"

class BinaryExpr(Node):
	def __init__(self, left, op, right):
		super()
		self.left = left
		self.op = op
		self.right = right
	
	def __repr__(self):
		return f"BinaryExpr ({self.left} {self.op} {self.right})"

class VarDeclaration(Node):
	def __init__(self, ident, value, type):
		super()
		self.ident = ident
		self.value = value
		self.type = type
	
	def __repr__(self):
		return f"VarDeclaration ({self.ident}: {self.type} = {self.value})"