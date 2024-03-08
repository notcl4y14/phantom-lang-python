from source.token import *

STR_WHITESPACE = " \t\n"
STR_OPERATORS = "+-*/%^=<>"
STR_CLOSURES = "()[]{}"
STR_SYMBOLS = ".,:;!|&"
STR_DIGITS = "1234567890"
STR_QUOTES = "\"'"
STR_IDENT_BREAK = " \t\n+-*/%=<>()[]{}.,:;!&|"
STR_ARR_KEYWORDS = ["let", "if", "else", "while", "for", "function"]
STR_ARR_LITERALS = ["null", "true", "false"]

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
	
	def yum(self, delta=1) -> str:
		prev = self.at()
		self.pos += delta
		return prev
	
	def not_eof(self) -> bool:
		return self.pos < len(self.code)
	
	# ===========================

	def lexerize(self):
		tokens = []

		while self.not_eof():
			char = self.at()

			if char in STR_WHITESPACE:
				pass
			elif char in STR_OPERATORS:
				tokens.append(Token("Operator", char))
			elif char in STR_CLOSURES:
				tokens.append(Token("Closure", char))
			elif char in STR_SYMBOLS:
				tokens.append(Token("Symbol", char))
			elif char in STR_DIGITS:
				tokens.append(self.lex_number())
			elif char in STR_QUOTES:
				tokens.append(self.lex_string())
			else:
				tokens.append(self.lex_ident())
			
			self.yum()
		
		tokens.append(Token("EOF"))
		
		return tokens
	
	def lex_number(self) -> Token:
		num_str = ""
		is_float = False

		while self.not_eof() and self.at() in STR_DIGITS + ".":
			num_str += self.at()
			
			if self.at() == ".":
				if is_float: break
				is_float = True
			
			self.yum()
		
		self.yum(-1)
		
		if is_float:
			return Token("Float", float(num_str))

		return Token("Int", int(num_str))
	
	def lex_string(self) -> Token:
		str = ""
		quote = self.yum()

		while self.not_eof() and self.at() != quote:
			str += self.yum()
		
		return Token("String", str)
	
	def lex_ident(self) -> Token:
		id_str = ""

		while self.not_eof() and not (self.at() in STR_IDENT_BREAK):
			id_str += self.yum()
		
		self.yum(-1)
		
		if id_str in STR_ARR_KEYWORDS:
			return Token("Keyword", id_str)
		elif id_str in STR_ARR_LITERALS:
			return Token("Literal", id_str)
		
		return Token("Ident", id_str)

def lexerize(code: str):
	lexer = Lexer(code)
	return lexer.lexerize()