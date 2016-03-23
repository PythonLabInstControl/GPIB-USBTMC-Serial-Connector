import time

class GenericDriver:
    def __init__(self, communicator, device_id, debug=False):
        self.communicator = communicator
        self.device_id = device_id
        self.debug = debug


    def get(self, cmd):
        self.communicator.flush()
        self.communicator.readline()
        
        self.write(cmd)
        ret = self.communicator.readline()
        ret = ret.rstrip()
        
        # Doing some bugfixing for the SR830 which gives sometimes ''
        #print('     ret = '+ret)
        #print(type(ret))
        if (ret == ''): print('Error "" ###### :'+ret); ret = self.get(cmd)
        elif (ret == ' '): print('Error " " ###### :'+ret); ret = self.get(cmd)
        elif (ret == '\n'): print('Error "\\n" ###### :'+ret); ret = self.get(cmd)
        elif (ret == '\r'): print('Error "\\r" ###### :'+ret); ret = self.get(cmd)
        return ret


    def set(self, cmd, param):
        self.write(cmd + " " + str(param))


    def write(self, cmd):
        self.communicator.write(unicode(cmd+"\n"))        
        time.sleep(0.05)
