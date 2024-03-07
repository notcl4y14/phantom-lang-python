from source.lexer import *

def main():
	tokens = lexerize("+-*/%^")
	print(tokens)

if __name__ == "__main__":
	main()