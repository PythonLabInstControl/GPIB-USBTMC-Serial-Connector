"""
Created on 18.11.2014
Veronika Schrenk

Modified by: Nico Leidenfrost, Philip Trauner

Required software:
- USBTMC: https://github.com/python-ivi/python-usbtmc
- PyUSB: https://github.com/walac/pyusb
"""

import TermOut.Logging as Logging
try:
	import usbtmc
except ImportException:
	Logging.error("usbtmc not installed")
from TermOut.ProgressBar import ProgressBar
import time
import subprocess
import sys
import Drivers.USBTMC

class USBTMC:
	def __init__(self, debug=False, display_discovered_devices=True):
		self.devices = {}
		self.drivers = {}
		self.debug = debug
		for i in dir(Drivers.USBTMC):
			if i[0] != "_" and i != "GenericDriver":
					driver = getattr(Drivers.USBTMC, i)
					if hasattr(driver, "DEVICES"):
						self.drivers.update(driver.DEVICES)
		if self.debug: Logging.header("Drivers for following devices have been loaded: %s" % self.drivers)
		Logging.header("Starting discovery of scientific USBTMC devices that do stuff.")
		devices = usbtmc.list_devices()
		progress_bar = ProgressBar(len(devices))
		progress = 0
		for device in devices:
			driver_avaliable = False
			inst = usbtmc.Instrument(device.idVendor, device.idProduct)
			device_id = inst.ask("*IDN?")
			for i in self.drivers:
				if i in device_id:
					self.devices[device_id] = self.drivers[i](inst)
					driver_avaliable = True
			if not driver_avaliable:
				self.devices[device_id] = Drivers.USBTMC.GenericDriver.GenericDriver(inst)
			progress += 1
			progress_bar.update(progress)
		if display_discovered_devices:
			for i in self.devices:
				Logging.header("%s discovered!" % i)
		Logging.success("Discovery finished successfully!")

	def __del__(self):
		self.close_usbtmc_devices()

	def close_usbtmc_devices(self):
		for device in self.devices:
			self.devices[device].communicator.reset()



if __name__ == "__main__":
	usb = USBTMC(debug=True, display_discovered_devices=False)
	port_table = {}
	virtual_port = 1
	for i in usb.devices:
		port_table[virtual_port] = i
		Logging.header("%s discovered on %s" % (i, str(virtual_port)))
		virtual_port += 1
	if len(usb.devices.keys()) > 0:
		port_corrent = False
		while not port_corrent:
			port = raw_input("Port: ")
			if port.isdigit():
				port = int(port)
				if port in port_table.keys():
					port_corrent = True
		Logging.header("Starting command line (^C to quit)")
		try:
			inst = usb.devices[port_table[port]]
			while 1:
				print(inst.get(raw_input("> ")))
		except KeyboardInterrupt:
			pass
