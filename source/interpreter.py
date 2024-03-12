from source.runtime_values import *
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
		return NumberValue(value_type, literal.value)
	
	def eval_StringLiteral(self, literal):
		return StringValue(literal.value)
	
	def eval_Literal(self, literal):
		if literal.value in ["true", "false"]:
			return BooleanValue(literal.value)
		
		return RuntimeValue(literal.value, None)
	
	def eval_BinaryExpr(self, expr):
		left = self.eval(expr.left)
		right = self.eval(expr.right)
		op = expr.op

		result = left.Operator(op.value, right)

		if result == None:
			return Error(f"Cannot do {left.type} {op.value} {right.type}", expr.pos)
			# return result
		
		return result

def interpret(ast):
	return Interpreter().eval(ast)