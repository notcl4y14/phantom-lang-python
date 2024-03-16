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
	
	def yumCheck(self, type, value):
		prev = self.at()

		if prev.type != type or prev.value != value:
			return None
		
		self.pos += 1
		return prev
	
	def not_eof(self):
		return self.at().type != "EOF"
	
	# ===========================

	def parse(self):
		program = Program().set_pos([self.tokens[0].pos[0], self.tokens[-1].pos[1]])

		while self.not_eof():
			if self.at().type == "Comment":
				self.yum()
				continue
			
			expr = self.parse_expr()

			if type(expr) == Error:
				return expr
			if expr != None:
				program.push(expr)
		
		return program
	
	# ===========================

	def parse_bin_expr(self, ops, func, _type = "Operator"):
		left = func()
		if type(left) == Error: return left

		while self.not_eof() and self.at().type == _type and self.at().value in ops:
			op = self.yum()

			right = func()
			if type(right) == Error:
				return Error("Expected a righthand value", right.pos)

			left = BinaryExpr(left, op, right).set_pos([left.pos[0], right.pos[1]])
		
		return left
	
	def parse_type(self):
		if self.at().type == "Symbol" and self.at().value == ":":
			self.yum()
		
		rt_type = self.parse_primary_expr()
		
		if rt_type is Identifier:
			return Error("Expected an identifier", rt_type.pos)
		
		return rt_type
	
	def parse_body(self, body):
		body = []

		while self.not_eof():
			if self.at().type == "Comment":
				self.yum()
				continue
			
			expr = self.parse_expr()

			if type(expr) == Error:
				return expr
			if expr != None:
				body.append(expr)
		
		return body
	
	# ===========================
	
	def parse_expr(self):
		if self.at().type == "Keyword" and self.at().value == "let":
			return self.parse_var_declaration()
		
		return self.parse_comp_expr()
	
	def parse_var_declaration(self):
		keyword = self.yum()
		name = self.yum()
		rt_type = self.parse_type()
		
		if type(rt_type) == Error: return rt_type

		if not (self.at().type == "Operator" and self.at().value == "="):
			return VarDeclaration(name, Literal("null"), rt_type).set_pos([keyword.pos[0], rt_type.pos[1]])
		
		self.yum() # Yum "="
		value = self.parse_expr()
		
		if type(value) == Error:
			return Error("Expected a value", value.pos)
		
		semicolon = self.yumCheck("Symbol", ";")
		right_pos = value.pos[1]

		if semicolon != None:
			right_pos = semicolon.pos[1]
		
		return VarDeclaration(name, value, rt_type).set_pos([keyword.pos[0], right_pos])
	
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
		elif token.type == "Ident":
			return Identifier(token.value).set_pos([token.pos[0], token.pos[1]])
		
		# Parenthesised expression
		elif token.type == "Closure" and token.value == "(":
			value = self.parse_expr()

			if not (self.at().type == "Closure" and self.at().value == ")"):
				return Error("Expected closing parenthesis", self.at().pos)
			
			self.yum()
			return value
		
		# Semicolon
		elif token.type == "Symbol" and token.value == ";":
			return None
		
		return Error("Unexpected token " + str(token), token.pos)

def parse(tokens):
	return Parser(tokens).parse()