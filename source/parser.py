from source.error import *
from source.nodes import *
# from nodes import *
# import nodes

class Parser:
	def __init__(self, tokens):
		self.tokens = tokens
		self.pos = -1

		self.yum()
	
	# ===========================
	
	def at(self):
		try:
			return self.tokens[self.pos]
		except:
			return None
	
	def yum(self):
		prev = self.at()
		self.pos += 1
		return prev
	
	def not_eof(self):
		return self.at().type != "EOF"
	
	# ===========================

	def parse(self):
		program = Program().set_pos([self.tokens[0].pos[0], self.tokens[-1].pos[1]])

		while self.not_eof():
			expr = self.parse_expr()

			if type(expr) == Error:
				return expr
			if expr != None:
				program.push(expr)
		
		return program
	
	# ===========================

	def parse_bin_expr(self, ops, func, type = "Operator"):
		left = func()

		while self.not_eof() and self.at().type == type and self.at().value in ops:
			op = self.yum()
			right = func()
			left = BinaryExpr(left, op, right).set_pos([left.pos[0], right.pos[1]])
		
		return left
	
	# ===========================
	
	def parse_expr(self):
		return self.parse_comp_expr()
	
	# ===========================

	def parse_logic_expr(self):
		return self.parse_bin_expr(["!", "&&", "||"], self.parse_comp_expr, "Symbol")

	def parse_comp_expr(self):
		return self.parse_bin_expr(["<", ">", "<=", ">=", "==", "!="], self.parse_add_expr)
	
	def parse_add_expr(self):
		return self.parse_bin_expr(["+", "-"], self.parse_mult_expr)
	
	def parse_mult_expr(self):
		return self.parse_bin_expr(["*", "/", "%"], self.parse_power_expr)
	
	def parse_power_expr(self):
		return self.parse_bin_expr(["^"], self.parse_primary_expr)
	
	# ===========================

	def parse_primary_expr(self):
		token = self.yum()

		# Values
		if token.type in ("Int", "Float"):
			return NumericLiteral(token.value).set_pos([token.pos[0], token.pos[1]])
		elif token.type == "String":
			return StringLiteral(token.value).set_pos([token.pos[0], token.pos[1]])
		elif token.type == "Literal":
			return Literal(token.value).set_pos([token.pos[0], token.pos[1]])
		
		# Parenthesised expression
		elif token.type == "Closure" and token.value == "(":
			value = self.parse_expr()

			if not (self.at().type == "Closure" and self.at().value == ")"):
				return Error("Expected closing parenthesis", self.at().pos)
			
			self.yum()
			return value

def parse(tokens):
	return Parser(tokens).parse()