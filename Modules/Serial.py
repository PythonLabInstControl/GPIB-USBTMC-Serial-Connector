import TermOut.Logging as Logging
try:
	import serial
except ImportException:
	Logging.error("pyserial not installed")
from TermOut.ProgressBar import ProgressBar
import os
import time
import sys
import Drivers.Serial

class Serial:
	def __init__(self, debug=False, baud=9600, timeout=1):
		self.devices = {}
		self.drivers = {}
		self.debug = debug
		for i in dir(Drivers.Serial):
			if i[0] != "_" and i != "GenericDriver":
					driver = getattr(Drivers.Serial, i)
					if hasattr(driver, "DEVICES"):
						self.drivers.update(driver.DEVICES)
		if self.debug: Logging.info("Drivers for following devices have been loaded: %s" % self.drivers)
		dev_devices = []
		for dev_device in os.listdir("/dev/"):
			if "USB" in dev_device:
				dev_devices.append(dev_device)
		progress_bar = ProgressBar(len(dev_devices))
		progress = 0
		device_number = 0
		for device in dev_devices:
			driver_avaliable = False
			inst = serial.Serial("/dev/" + device, baud, timeout=timeout)
			time.sleep(0.1)
			inst.write("*IDN?\r\n")
			time.sleep(0.1)
			device_id = inst.readline().rstrip()
			for i in self.drivers:
				if i in device_id:
					self.devices[device_number] = self.drivers[i](inst, device_id)
					driver_avaliable = True
			if not driver_avaliable:
				self.devices[device_number] = Drivers.Serial.GenericDriver.GenericDriver(inst, device_id)
			progress += 1
			device_number += 1
			progress_bar.update(progress)
		for i in self.devices:
			Logging.header("%s discovered on virtual port %s" % (self.devices[i].device_id, i))
		Logging.success("Discovery finished successfully!")

	def __del__(self):
		pass
	"""
	def close_usbtmc_devices(self):
		for device in self.devices:
			self.devices[device].communicator.reset()
	"""


if __name__ == "__main__":
	s = Serial(debug=True)
	if len(s.devices.keys()) > 0:
		port_corrent = False
		while not port_corrent:
			port = raw_input("Port: ")
			if port.isdigit():
				port = int(port)
				if port in s.devices.keys():
					port_corrent = True
		Logging.header("Starting command line (^C to quit)")
		try:
			inst = s.devices[port]
			while 1:
				print(inst.get(raw_input("> ")))
		except KeyboardInterrupt:
			pass
