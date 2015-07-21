class GenericDriver:
	def __init__(self, communicator, debug=False):
		self.communicator = communicator
		self.debug = debug


	def get(self, cmd):
		self.communicator.write(cmd)
		return self.communicator.read(1024)


	def set(self, cmd, param):
		self.communicator.write(cmd + " " + str(param))