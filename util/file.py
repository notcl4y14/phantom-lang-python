def read_file(filename: str, encoding: str = "utf-8"):
	file = None

	try:
		file = open(filename, encoding=encoding)
	except:
		return None
	
	return file.read()