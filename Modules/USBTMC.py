"""
Created by: Nico Leidenfrost, Philip Trauner

Required software:
- USBTMC: https://github.com/python-ivi/python-usbtmc
- PyUSB: https://github.com/walac/pyusb
"""

import TermOut.Logging as Logging
try:
	import usbtmc
except ImportException:
	Logging.error("usbtmc not installed")
	exit(1)
from TermOut.ProgressBar import ProgressBar
import os
import time
import subprocess
import sys
import Drivers.USBTMC

class USBTMC:
	def __init__(self, debug=False):
		if os.geteuid() != 0:
			Logging.error("You need to have root privileges to run this script.")
			self.started = False
			exit(1)
		self.started = True
		self.devices = {}
		self.drivers = {}
		self.debug = debug
		for i in dir(Drivers.USBTMC):
			if i[0] != "_" and i != "GenericDriver":
					driver = getattr(Drivers.USBTMC, i)
					if hasattr(driver, "DEVICES"):
						self.drivers.update(driver.DEVICES)
		if self.debug: Logging.info("Drivers for following devices have been loaded: %s" % self.drivers)
		devices = usbtmc.list_devices()
		progress_bar = ProgressBar(len(devices))
		progress = 0
		device_number = 0
		for device in devices:
			driver_avaliable = False
			inst = usbtmc.Instrument(device.idVendor, device.idProduct, device.serial_number)
			device_id = inst.ask("*IDN?")
			for i in self.drivers:
				if i in device_id:
					self.devices[device_number] = self.drivers[i](inst, device_id)
					driver_avaliable = True
			if not driver_avaliable:
				self.devices[device_number] = Drivers.USBTMC.GenericDriver.GenericDriver(inst, device_id)
			progress += 1
			device_number += 1
			progress_bar.update(progress)
		for i in self.devices:
			Logging.header("%s discovered on virtual port %s" % (self.devices[i].device_id, i))
		Logging.success("Discovery finished successfully!")

	def __del__(self):
		self.close_usbtmc_devices()

	def close_usbtmc_devices(self):
		if self.started:
			for device in self.devices:
				self.devices[device].communicator.reset()



if __name__ == "__main__":
	usb = USBTMC(debug=True)
	if len(usb.devices.keys()) > 0:
		port_corrent = False
		while not port_corrent:
			port = raw_input("Port: ")
			if port.isdigit():
				port = int(port)
				if port in usb.devices.keys():
					port_corrent = True
		Logging.header("Starting command line (^C to quit)")
		try:
			inst = usb.devices[port]
			while 1:
				print(inst.get(raw_input("> ")))
		except KeyboardInterrupt:
			pass
