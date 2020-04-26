from Devices import Devices
import time

class TimeSensor(Devices):

    '''
    Tempreture IS the time for time sensors
    '''
    def __init__(self, id, name, time = 0):
        self.time = time
        super().__init__(id, name)
    
    '''
    Returns : objects main reading, in this case time
    '''
    def getReading(self):
        self.time = time.time()
        return self.time
    
    '''
    Converts object to string

    return: string representaion of object
    '''
    def toStringFormat(self):
        return "Name: " + str(self.name) + " ID: " + str(self.id) + " Time: " + str(self.time)