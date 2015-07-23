from Serial import Serial

s = Serial(debug=True)

for i in s.devices:
	if "hmp2030" in s.devices[i].device_id.lower():
		while 1:
			s.devices[0].write("SYSTem:BEEPer[:IMMediate]")
