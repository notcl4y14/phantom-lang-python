from source.token import *
from source.position import *

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
	def __init__(self, filename: str, code: str):
		self.code = code
		self.pos = Position(filename, -1, 0, -1)
		
		self.yum()
	
	# ===========================
	
	def at(self, delta = 0) -> str:
		try:
			return self.code[self.pos.index + delta]
		except:
			return ""
	
	def at_range(self, range = 0, delta = 0) -> str:
		try:
			return self.code[(self.pos.index + delta):(self.pos.index + range + delta)]
		except:
			return ""
	
	def yum(self, delta=1) -> str:
		prev = self.at()
		self.pos.advance(self.at(), delta)
		return prev
	
	def not_eof(self) -> bool:
		return self.pos.index < len(self.code)
	
	# ===========================

	def lexerize(self):
		tokens = []

		while self.not_eof():
			char = self.at()
			pos = self.pos.clone()

			if char in STR_WHITESPACE:
				pass
			elif char in STR_OPERATORS:

				# Allows operators like +=, <=, >=, ==
				if self.at(1) == "=":
					tokens.append(Token("Operator", char + self.at(1)).set_pos([pos, pos.advance()]))

					# Prevents the line from adding a new token
					self.yum(2)
					continue
				
				# Comments
				elif self.at() == "/" and self.at(1) in "/*":
					tokens.append(self.lex_comment())
					self.yum()
					continue
				
				# That line
				tokens.append(Token("Operator", char).set_pos([pos, pos.advance()]))

			elif char in STR_CLOSURES:
				tokens.append(Token("Closure", char).set_pos([pos, pos.advance()]))
			elif char in STR_SYMBOLS:

				# Allows operators like &&, || and !=. Also != is an operator
				# Some lasagna code
				if self.at(1) == char or (char == "!" and self.at(1) == "="):
					if char == "!":
						tokens.append(Token("Operator", char + self.at(1)).set_pos([pos, pos.advance()]))
						self.yum(2)
						continue
					
					tokens.append(Token("Symbol", char + self.at(1)).set_pos([pos, pos.advance()]))
					self.yum(2)
					continue

				tokens.append(Token("Symbol", char).set_pos([pos, pos.advance()]))

			elif char in STR_DIGITS:
				tokens.append(self.lex_number())
			elif char in STR_QUOTES:
				tokens.append(self.lex_string())
			else:
				tokens.append(self.lex_ident())
			
			self.yum()
		
		tokens.append(Token("EOF").set_pos([self.pos.clone(), self.pos.clone()]))
		
		return tokens
	
	def lex_number(self) -> Token:
		left_pos = self.pos.clone()
		num_str = ""
		is_float = False

		while self.not_eof() and self.at() in STR_DIGITS + ".":
			num_str += self.at()
			
			if self.at() == ".":
				if is_float: break
				is_float = True
			
			self.yum()
		
		right_pos = self.pos.clone()
		
		self.yum(-1)
		
		if is_float:
			return Token("Float", float(num_str)).set_pos([left_pos, right_pos])

		return Token("Int", int(num_str)).set_pos([left_pos, right_pos])
	
	def lex_string(self) -> Token:
		left_pos = self.pos.clone()
		str = ""
		quote = self.yum()

		while self.not_eof() and self.at() != quote:
			str += self.yum()
		
		right_pos = self.pos.clone()

		return Token("String", str).set_pos([left_pos, right_pos])
	
	def lex_ident(self) -> Token:
		left_pos = self.pos.clone()
		id_str = ""

		while self.not_eof() and not (self.at() in STR_IDENT_BREAK):
			id_str += self.yum()
		
		right_pos = self.pos.clone()

		self.yum(-1)
		
		if id_str in STR_ARR_KEYWORDS:
			return Token("Keyword", id_str).set_pos([left_pos, right_pos])
		elif id_str in STR_ARR_LITERALS:
			return Token("Literal", id_str).set_pos([left_pos, right_pos])
		
		return Token("Ident", id_str).set_pos([left_pos, right_pos])
	
	def lex_comment(self) -> Token:
		if self.at(1) == "/":
			return self.lex_comment_one()
		elif self.at(1) == "*":
			return self.lex_comment_multi()
	
	def lex_comment_one(self) -> Token:
		left_pos = self.pos.clone()
		comment_str = ""

		self.yum(2)          # Yum "//"

		while self.not_eof() and self.at() != "\n":
			comment_str += self.yum()
		
		right_pos = self.pos.clone()

		return Token("Comment", comment_str).set_pos([left_pos, right_pos])
	
	def lex_comment_multi(self) -> Token:
		left_pos = self.pos.clone()
		comment_str = ""
		# closure_count = 1

		self.yum(2)          # Yum "/*"

		# while self.not_eof() and closure_count < 0:
			# print(self.at_range(2), self.at_range(2) == "*/")
			# if self.at_range(2) == "/*":
				# closure_count += 1
			# elif self.at_range(2) == "*/":
				# closure_count -= 1
			
			# print(self.at())
		while self.not_eof() and self.at_range(2) != "*/":
			comment_str += self.yum()
		
		self.yum() # Yum slash in "*/"
		right_pos = self.pos.clone()

		return Token("Comment", comment_str).set_pos([left_pos, right_pos])

def lexerize(filename: str, code: str):
	lexer = Lexer(filename, code)
	return lexer.lexerize()