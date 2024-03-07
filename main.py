import sys
from source.lexer import *
from util.file import *

def run(code: str, flags):
	tokens = lexerize(code)

	if "--lexer" in flags:
		print(tokens)

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

	run(code, flags)

if __name__ == "__main__":
	sys.argv.pop(0)

	main()