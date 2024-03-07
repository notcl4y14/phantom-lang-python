from source.token import *

class Lexer:
	def __init__(self, code: str):
		self.code = code
		self.pos = -1
		
		self.yum()
	
	# ===========================
	
	def at(self) -> str:
		try:
			return self.code[self.pos]
		except:
			return ""
	
	def yum(self) -> str:
		prev = self.at()
		self.pos += 1
		return prev
	
	def not_eof(self) -> bool:
		return self.pos < len(self.code)
	
	# ===========================

	def lexerize(self):
		tokens = []

		while self.not_eof():
			char = self.at()

			if char in "+-*/%^":
				tokens.append(Token("Operator", char))
			
			self.yum()
		
		return tokens

def lexerize(code: str):
	lexer = Lexer(code)
	return lexer.lexerize()