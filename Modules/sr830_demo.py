from GPIB import GPIB

g = GPIB()
print("Devices: " + str(g.devices))
port = int(raw_input("Port: "))
i = 1
while 1:
	print("%s: %s" % (str(i), g.devices[2].getR()))
	i += 1