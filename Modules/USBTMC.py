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
	print(usb.devices)