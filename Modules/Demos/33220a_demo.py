from USBTMC import USBTMC

usb = USBTMC(debug=True)
for i in usb.devices:
	if "33220a" in usb.devices[i].device_id.lower():
		print("Beeper state: %s" % ("ON" if usb.devices[i].get_beeper_state() == "1" else "OFF"))
				
