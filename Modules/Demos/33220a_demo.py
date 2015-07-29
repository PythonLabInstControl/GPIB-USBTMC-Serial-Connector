from USBTMC import USBTMC
import time

usb = USBTMC(debug=True)
for i in usb.devices:
        if "33220a" in usb.devices[i].device_id.lower():
                if usb.devices[i].get_beeper_state() == "1":
			while usb.devices[i].get("FREQ?") != "+7.3556080000000E+00":
				print("JETZT!!!")
				time.sleep(7)
                        delay = 1
                        bombboomtime = 45
                        j = 0
                        mult = 1
                        while bombboomtime > 0:
                                if delay < 0:
                                        delay = 0.01
                                        bombboomtime = -420
                                usb.devices[i].communicator.write("SYSTem:BEEPer")
                                time.sleep(delay)
                                delay -= 0.01 * mult
                                mult += 0.00337
                                j += 1
                                bombboomtime -= delay
			for k in range(3):
				usb.devices[i].communicator.write("SYSTem:BEEPer")
				time.sleep(0.0425218)
