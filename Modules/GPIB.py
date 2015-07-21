import TermOut.Logging as Logging
try:
	import gpib
except ImportError:
	Logging.error("linux_gpib not installed or Python bindings not built")
	exit(1)
from TermOut.ProgressBar import ProgressBar
import os
import subprocess
import time
import sys
import Drivers


class GPIB:
	def __init__(self, sad=0, timeout=13, send_eoi=1, eos_mode=0, debug=False, interfaces=[]):
		self.debug = debug
		self.devices = {}
		self.drivers = {}
		# We go through each driver and look at the attribute DEVICES which contains all devices the driver should be loaded for.
		for i in dir(Drivers):
        		if i[0] != "_" and i != "GenericGPIBDriver":
                		driver = getattr(Drivers, i)
                		if hasattr(driver, "DEVICES"):
					for k in driver.DEVICES:
                                		if k in self.drivers.keys():
                                			Logging.warning("%s and %s support the same device." % (self.drivers[k], driver))
                                		self.drivers[k] = getattr(driver, i) 
				else:
					Logging.warning("'DEVICES' attribute missing for %s" % driver)
		if self.debug: Logging.header("Drivers for following devices have been loaded: %s" % self.drivers)
		self.started = True
		self.reset_usb_controller()
		# Interface ids are used to determine which usb connections need to be reset
		# Example:
		"""
		Bus 001 Device 006: ID 3923:709b National Instruments Corp. GPIB-USB-HS
		"""
		self.interfaces = ["3923:709b", "0957:0518"] + interfaces
		if os.geteuid() != 0:
			Logging.error("You need to have root privileges to run this script.")
			self.started = False
			exit(1)
		self.reset_interfaces()
		Logging.header("Starting discovery of scientific devices that do stuff")
		progress_bar = ProgressBar(30)
		discovered = {}
		for pad in range(0, 31):
			id = gpib.dev(0, pad, sad, timeout, send_eoi, eos_mode)
			try:
				driver_avaliable = False
				gpib.clear(id)
				gpib.write(id, "*IDN?")
				device_id = gpib.read(id, 1024).rstrip()
				for i in self.drivers:
					if i in device_id:
						self.devices[pad] = self.drivers[i](GPIBCommunicator(id, self.reset_interfaces))
						driver_avaliable = True
				if not driver_avaliable:
					self.devices[pad] = Drivers.GenericGPIBDriver.GenericGPIBDriver(GPIBCommunicator(id, self.reset_interfaces))
				discovered[id] = device_id
			except gpib.GpibError:
				pass
			progress_bar.update(pad)
		for i in discovered:
			Logging.header("%s on %s" % (discovered[i], i - 16))
		Logging.success("Discovery finished successfully!")



	def __del__(self):
		for i in self.devices:
			gpib.close(i.communicator.id)
		self.reset_usb()


	def reset_usb_controller(self):
		if self.debug: Logging.warning("Resetting usb controller")
		os = open("/etc/issue").read()
		if os == 'Debian GNU/Linux 8 \\n \\l\n\n' or os == 'Debian GNU/Linux  \\n \\l\n\n':
			self.reset_debian()


	def reset_debian(self):
		ehci_content = os.listdir("/sys/bus/pci/drivers/ehci-pci/")
		for i in ehci_content:
			if i[0] == "0":
				os.system('echo -n %s | sudo tee /sys/bus/pci/drivers/ehci-pci/unbind' % i)
				os.system('echo -n %s | sudo tee /sys/bus/pci/drivers/ehci-pci/bind' % i)


	def reset_usb(self):
		if self.debug: Logging.info("Resetting connected usb interfaces")
		for i in subprocess.check_output(["lsusb"]).split("\n"):
			for k in self.interfaces:
				if k in i:
					try:
						subprocess.check_output(["sudo", "usbreset", "/dev/bus/usb/%s/%s" % (i[4:7], i[15:18])])
					except subprocess.CalledProcessError:
						self.reset_usb_controller()




	# If the interface get's stuck this function is used to reset it
	def reset_interfaces(self, calls=0):
		if self.debug: Logging.info("Resetting connected interfaces")
		self.reset_usb()
		time.sleep(2)
		if self.debug: Logging.info("Running gpib_config")
		try:
			subprocess.check_call(["sudo", "gpib_config"])
		except subprocess.CalledProcessError:
			if calls == 2:
				Logging.error("No interface connected")
				exit(1)
			self.reset_interfaces(calls=calls + 1)
		time.sleep(2)


class GPIBCommunicator:
	def __init__(self, id, reset, debug=False):
		self.id = id
		self.reset = reset
		self.last_write = ""

	def __str__(self):
		return "GPIB adress: %s" % self.id

	def command(self, str):
		gpib.command(self.id, str)


	def config(self, option, value):
		self.res = gpib.config(self.id, option, value)
		return self.res


	def interface_clear(self):
		gpib.interface_clear(self.id)


	def write(self, str, calls=0):
		try:
			gpib.write(self.id, str)
			self.last_write = str
		except gpib.GpibError:
			if calls == 2:
				Logging.error("Unrecoverable error. Please reboot")
				raw_input("Press ENTER when done.")
				exit(1)
			self.reset()
			self.write(str, calls=calls + 1)


	def write_async(self, str):
		gpib.write_async(self.id, str)


	def read(self, len=512, calls=0):
		try:
			result = gpib.read(self.id, len).rstrip("\n")
		except gpib.GpibError, e:
			Logging.warning(str(e))
			if str(e) == "read() failed: A read or write of data bytes has been aborted, possibly due to a timeout or reception of a device clear command.":
				Logging.info("Last write didn't succeed. Resending...")
				self.reset()
				self.write(self.last_write)
			if calls == 2:
				Logging.error("Unrecoverable error. Please reboot")
				raw_input("Press ENTER when done.")
				exit(1)
			self.reset()
			result = self.read(calls=calls + 1)
		return result


	def listener(self, pad, sad=0):
		self.res = gpib.listener(self.id, pad, sad)
		return self.res


	def ask(self,option):
		self.res = gpib.ask(self.id, option)
		return self.res


	def clear(self):
		gpib.clear(self.id)


	def wait(self, mask):
		gpib.wait(self.id, mask)


	def serial_poll(self):
		self.spb = gpib.serial_poll(self.id)
		return self.spb


	def trigger(self):
		gpib.trigger(self.id)


	def remote_enable(self, val):
		gpib.remote_enable(self.id, val)


	def ibloc(self):
		self.res = gpib.ibloc(self.id)
		return self.res


	def ibsta(self):
		self.res = gpib.ibsta()
		return self.res


	def ibcnt(self):
		self.res = gpib.ibcnt()
		return self.res


	def timeout(self, value):
		return gpib.timeout(self.id, value)

if __name__ == "__main__":
	g = GPIB(debug=True)
	if len(g.devices.keys()) > 0:
		Logging.header(g.devices.keys())
		port_corrent = False
		while not port_corrent:
			port = raw_input("Port: ")
			if port.isdigit():
				port = int(port)
				if port in g.devices.keys():
					port_corrent = True
		Logging.header("Starting command line (^C to quit)")
		try:
			while 1:
				print(g.devices[port].get(raw_input("> ")))
		except KeyboardInterrupt:
			pass
