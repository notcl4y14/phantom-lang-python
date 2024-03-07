from source.lexer import *

def main():
	tokens = lexerize("let x = 10 + 4 - 5; let y = \"lol\"; let a = true; let π = 3.14;")
	print(tokens)

if __name__ == "__main__":
	main()