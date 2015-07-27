from USBTMC import USBTMC
from GPIB import GPIB
from Serial import Serial
import time
import TermOut.Logging as Logging

usb = USBTMC()
gpib = GPIB()
serial = Serial()

devices = []

for i in usb.devices:
	devices.append(usb.devices[i])

for i in gpib.devices:
	devices.append(gpib.devices[i])

for i in serial.devices:
	devices.append(serial.devices[i])

print(devices)
while 1:
	k = 0
	for i in devices:
		Logging.info(i.get("*IDN?").rstrip())
		k += 1
	Logging.header("Got answer from %s devices." % str(k))
	time.sleep(2)
