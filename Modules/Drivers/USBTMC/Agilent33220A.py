from GenericDriver import GenericDriver

class Agilent33220A(GenericDriver):
	def get_beeper_state(self):
		return self.get("system:beeper:state?")
	

	def set_beeper_state(self, state):
                self.write("system:beeper:state %s" % ("1" if state else "0"))


	def beep(self):
		self.write("syst:beep")


	def get_frequency(self):
		return float(self.get("frequency?"))


	def set_frequency(self, freq, unit="HZ"):
		 self.write("frequency %s %s" % (str(freq), unit))

	
	def get_min_frequency(self):
		return float(self.get("frequency? min"))


	def get_max_frequency(self):
		return float(self.get("frequency? max"))

	
	def get_function(self):
		return self.get("function?")


	def set_function(self, function):
		functions = {0 : "SIN", 1 : "SQU", 2 : "RAMP", 3 : "PULS", 4 : "NOIS", 5 : "DC", 6 : "USER"}     
		if function in functions.keys():
			self.write("function %s" % functions[function])
		elif function in functions.values():
			self.write("function %s" % function)
		else:
			raise FunctionNotAvaliableException("Function %s not avaliable" % str(function))

	
	def get_output_state(self):
		return True if self.get("outp?") == "1" else False

	
	def set_output_state(self, state):
		if state:
			self.write("outp on")
		else:
			self.write("outp off")


	def get_max_load(self):
		return float(self.get("output:load? min"))


	def get_min_load(self):
		return float(self.get("output:load? max"))


	def get_load(self):
		return float(self.get("output:load?"))

	
	def set_load(self, load):
		self.write("output:load %s" % str(load))


	def get_min_offset(self):
		return float(self.get("voltage:offset? min"))


	def get_max_offset(self):
		return float(self.get("voltage:offset? max"))


	def get_offset(self):
		return float(self.get("voltage:offset?"))	


	def set_offset(self, offset, unit="V"):
		self.write("voltage:offset %s %s" % (str(offset), unit))

	
	def get_voltage(self):
		return float(self.get("voltage?"))		


	def set_voltage(self, voltage, unit="Vpp"):
		self.write("voltage %s %s" % (str(voltage), unit))


	

class FunctionNotAvaliableException(Exception):
	def __init__(self, message):
		super(FunctionNotAvaliableException, self).__init__(message)
		self.message = message
		

DEVICES = {"33220A" : Agilent33220A}
