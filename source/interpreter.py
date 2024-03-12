from source.runtime_value import *
from source.error import *

class Interpreter:
	def __init__(self):
		pass

	def eval(self, expr):
		method_name = "eval_" + str(expr.__class__.__name__)
		method = None

		try:
			method = self.__getattribute__(method_name)
		except:
			pass

		if method == None:
			return Error("Undefined AST type for interpretation: \"" + method_name + "\"", expr.pos)
		
		return method(expr)
	
	def eval_Program(self, program):
		last = None

		for expr in program.body:
			last = self.eval(expr)
			
			if last is Error:
				break
		
		return last
	
	def eval_NumericLiteral(self, literal):
		value_type = type(literal.value).__name__
		return RuntimeValue(value_type, literal.value)

def interpret(ast):
	return Interpreter().eval(ast)