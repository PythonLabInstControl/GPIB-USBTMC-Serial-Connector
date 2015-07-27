class GenericDriver:
	def __init__(self, communicator, device_id, debug=False):
		self.communicator = communicator
		self.device_id = device_id
		self.debug = debug


	def get(self, cmd):
		self.communicator.write(cmd)
		return self.communicator.read(1024)


	def set(self, cmd, param):
		self.communicator.write(cmd + " " + str(param))
	

	def write(self, cmd):
		self.communicator.write(cmd)
