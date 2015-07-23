from GenericDriver import GenericDriver

class Agilent33220A(GenericDriver):
	def get_beeper_state(self):
		return self.get("system:beeper:state?")

DEVICES = {"33220A" : Agilent33220A}
