import time

class GenericDriver:
	def __init__(self, communicator, device_id, debug=False):
		self.communicator = communicator
		self.device_id = device_id
		self.debug = debug


	def get(self, cmd):
		self.write(cmd)
		return self.communicator.readline()


	def set(self, cmd, param):
		self.write(cmd + " " + str(param))


	def write(self, cmd):
		self.communicator.write(cmd + "\r\n")
		time.sleep(0.1)
