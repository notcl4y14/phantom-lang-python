class RuntimeValue:
	def __init__(self, type, value):
		self.type = type
		self.value = value
	
	def Operator(self, op, right):
		pass

	def create_from_value(value):
		value_type = type(value).__name__

		if value_type == "str":
			return StringValue(value)
		elif value_type in ["int", "float"]:
			return NumberValue(value_type, value)
	
	def __repr__(self):
		return str(self.type) + ": " + str(self.value)

class NumberValue(RuntimeValue):
	def __init__(self, type, value):
		super().__init__(type, value)
	
	def Operator(self, op, right):
		if not right.type in ["int", "float"]:
			return None
		
		result = None

		if op == "+":
			result = self.value + right.value
		elif op == "-":
			result = self.value - right.value
		elif op == "*":
			result = self.value * right.value
		elif op == "/":
			# Had to do some little of a lasagna code here
			# TODO: Replace with an Infinity type when it's added
			if right.value == 0:
				result = "Infinity"
			else:
				result = self.value / right.value

				# Converting float back to int if it's the same 
				if result == int(result):
					result = int(result)
			
		elif op == "%":
			result = self.value % right.value
		elif op == "^":
			result = self.value ^ right.value
		
		return RuntimeValue.create_from_value(result)

class StringValue(RuntimeValue):
	def __init__(self, value):
		super().__init__("string", value)
	
	def Operator(self, op, right):
		if not right.type in ["str", "int"]:
			return None
		
		result = None

		if op == "+":
			result = self.value + right.value
		elif op == "*":
			if right.type == "str":
				return None
			
			result = self.value * right.value
		else:
			return None
		
		return RuntimeValue.create_from_value(result)

class BooleanValue(RuntimeValue):
	def __init__(self, value):
		super().__init__("boolean", value)
	
	def Operator(self, op, right):
		# TODO: Probably make boolean convert
		#       itself into a number value and
		#       do the operator stuff :P
		return None