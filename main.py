import sys
from source.error import *
from source.lexer import *
from source.parser import *
from util.file import *

def repr(name, contents, line_width = 24):
	top_line_width = line_width - (len(name) + 1)

	# print(f"{name} {top_line_width}")
	print(name, end=" ")
	for i in range(0, top_line_width):
		print("=", end="")
	print()
	print(contents)
	for i in range(0, line_width):
		print("=", end="")
	print()

def run(filename: str, code: str, flags):
	tokens = lexerize(filename, code)

	if "--lexer" in flags:
		repr("Tokens", tokens)
	
	ast = parse(tokens)

	if type(ast) == Error:
		print(ast)
		return

	if "--parser" in flags:
		repr("AST", ast)

def main():
	args = sys.argv

	if len(args) == 0:
		print("ERROR: Filename should be specified!")
		return

	filename = args[0]
	code = read_file(filename)

	if code == None:
		print(f"ERROR: Filename \"{filename}\" not found!")
		return
	
	flags = args
	flags.pop(0)

	run(filename, code, flags)

if __name__ == "__main__":
	sys.argv.pop(0)

	main()