from GPIB import GPIB

g = GPIB()
print("Devices: " + str(g.devices))
if len(g.devices) > 0:
	port = int(raw_input("Port: "))
	i = 1
	while 1:
		print("%s: %s" % (str(i), g.devices[port].getR()))
		i += 1
