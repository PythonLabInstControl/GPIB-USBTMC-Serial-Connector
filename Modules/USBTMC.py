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


class USBTMC:
	def __init__(self, debug=False):
		self.devices = {}
		self.debug = debug
		Logging.header("Starting discovery of scientific USBTMC devices that do stuff.")
		devices = usbtmc.list_devices()
		progress_bar = ProgressBar(len(devices))
		progress = 0
		for device in devices:
			inst = usbtmc.Instrument(device.idVendor, device.idProduct)
			self.devices[inst.ask("*IDN?")] = inst
			progress += 1
			progress_bar.update(progress)
		for i in self.devices:
			Logging.info("%s discovered!" % i)

	def __del__(self):
		self.close_usbtmc_devices()

	def close_usbtmc_devices(self):
		for device in self.devices:
			usbtmc.Instrument.reset(self.devices[device])


if __name__ == "__main__":
	usb = USBTMC(debug=True)
	devices = usbtmc.list_devices()
	device_list = {}
	i = 1
	for device in devices:
		inst = usbtmc.Instrument(device.idVendor, device.idProduct)
		device_list[i] = inst.ask("*IDN?")
		i += 1
	for i in device_list:
		Logging.header("%s on %s" % (device_list[i], i))
	Logging.success("Discovery finished successfully!")
	if len(device_list.keys()) > 0:
		port_corrent = False
		while not port_corrent:
			port = raw_input("Port: ")
			if port.isdigit():
				port = int(port)
				if port in device_list.keys():
					port_corrent = True
		Logging.header("Starting command line (^C to quit)")
		try:
			inst = usbtmc.Instrument(devices[port - 1].idVendor, devices[port - 1].idProduct)
			while 1:
				print(inst.ask(raw_input("> ")))
		except KeyboardInterrupt:
			pass
