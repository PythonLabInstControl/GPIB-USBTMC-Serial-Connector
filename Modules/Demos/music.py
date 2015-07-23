from USBTMC import USBTMC
from GPIB import GPIB
import time

usb = USBTMC()
gpib = GPIB()

usb_beep = []
gpib_beep = []

for i in usb.devices:
	if "33220a" in usb.devices[i].device_id.lower():
		usb_beep.append(usb.devices[i])

for i in gpib.devices:
	if "m3500a" in gpib.devices[i].device_id.lower():
		gpib_beep.append(gpib.devices[i])

for i in range(100):
	for i in usb_beep:
		i.communicator.write("system:beep")
	time.sleep(0.3)
	for i in gpib_beep:
		i.communicator.write("system:beep")
	time.sleep(0.3)
