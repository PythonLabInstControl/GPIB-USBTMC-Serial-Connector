import time

class HMP2030:
    def __init__(self, communicator, device_id, debug=False):
        self.communicator = communicator
        self.device_id = device_id
        self.debug = debug


    def get(self, cmd):
        self.write(cmd)
        return self.readline()


    def set(self, cmd, param):
        self.write(cmd + " " + str(param))


    def write(self, cmd):
        self.write(cmd + "\r\n")
        time.sleep(0.1)




    def RST(self):
        # ReSeT
        self.write('*RST')

    def beep(self):
        self.write("SYSTem:BEEPer[:IMMediate]")
        time.sleep(0.1)


    def set_INSTrumentNSELect(self, i_output):
        # Selects a channel. Each channel of the power supply is considered as separate    instrument, which is required by the SCPI  standart.
        # The given input has to be 1, 2, or 3
        
        exception_text = "The given input has to be 1, 2, or 3";

        try:
            i_output = int(i_output)
        except:
            raise Exception(exception_text)
        if i_output < 1 or i_output > 3 or not(isinstance( i_output, ( int, long ) )):
            raise Exception(exception_text)

        self.set("INSTrument:NSELect", i_output)


    def get_INSTrumentSELect(self):
     # Selects a channel. Each channel of the power supply is considered as separate "instrument, which is required by the SCPI  standart"

        i_output = self.get("INSTrument:SELect?",)
        return i_output

    def set_OUTPutGENeral(self, switch):
        # 1 or 0 to set all outputs on or off
        exception_text = "1 or 0 to set all outputs on or off"

        try:
            switch = int(switch)
        except:
            raise Exception(exception_text)
            
        if switch < 0 or switch > 1 or not(isinstance( switch, ( int, long ) )):
            raise Exception(exception_text)
        self.set("OUTPutGENeral", switch)

    def set_OUTPutGENeralON(self):
        # set all outputs on

        self.write("OUTPutGENeral ON")

    def set_OUTPutGENeralOFF(self):
        # set all outputs off

        self.write("OUTPutGENeral OFF")

    def get_OUTPutGENeral(self):
     # 
        output = self.write("OUTPutGENeral?")
        return output

    def set_OUTPutSELectON(self):
        # Activates the previous selected channel. If the channel is activated the channel
        # LED lights up green in CV (constant voltage) mode or red in CC (constant current) mode.
        self.set("OUTPut:SELect", 1)

    def set_OUTPutSELectOFF(self):
        # Deactivates the previous selected channel. If the channel is activated the channel
        # LED lights up green in CV (constant voltage) mode or red in CC (constant current) mode.
        self.set("OUTPut:SELect", 0)


    def set_OUTPutSTATeON(self):
        # Activates the previous selected channel and turning on the output. The selected
        #channel LED lights up green. If the output will be turned of with OUTP OFF only the previous
        #selected channel will be deactivated. After sending OUTP OFF command the output button is
        #still activated.

        self.set("OUTPut:STATe", 1)

    def set_OUTPutSTATeOFF(self):
        # Deactivates the previous selected channel and turning on the output. The selected
        #channel LED lights up green. If the output will be turned of with OUTP OFF only the previous
        #selected channel will be deactivated. After sending OUTP OFF command the output button is
        #still activated.

        self.write("OUTPut:STATe OFF")



    def set_SOURceVOLTageLEVel(self, input):
        
        try: 
            (input == float(input))|(input == int(input))
        except:
            raise Exception("Given input is not of type float of int.")
        
        if (input == float(input))|(input == int(input) ):
            self.set("SOURce:VOLTage:LEVel:IMMediate:AMPLitude", input)

    def set_SOURceVOLTageLEVelMIN(self):
        self.write('SOURce:VOLTage:LEVel:IMMediate:AMPLitude MIN')
        
    def set_SOURceVOLTageLEVelMAX(self):
        self.write('SOURce:VOLTage:LEVel:IMMediate:AMPLitude MAX')
        
        
        
    def set_SOURceCURRentLEVel(self, input):
        # Sets the current value of the selected channel.
        
        try: 
            (input == float(input))|(input == int(input))
        except:
            raise Exception("Given input is not of type float of int.")
        
        if (input == float(input))|(input == int(input) ):
            self.set("SOURce:CURRent:LEVel:IMMediate:AMPLitude", input)

    def set_SOURceCURRentLEVelMIN(self):
        # Sets the current value of the selected channel.
        # Current value depending on the instrument type.
        #   MIN	
        #   0.5mA (5A channel) / 1mA (10A channel)
        self.write('SOURce:CURRent:LEVel:IMMediate:AMPLitude MIN')
        
    def set_SOURceCURRentLEVelMAX(self):
        # Sets the current value of the selected channel.
        # Current value depending on the instrument type.
        #   MAX
        #   10.010A (HMP2020 / HMP2030 / HMP4030 / HMP4040)
        self.write('SOURce:CURRent:LEVel:IMMediate:AMPLitude MAX')
        



DEVICES = {"HMP2030" : HMP2030}
