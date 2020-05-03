from Devices import Devices

class Sensor(Devices):

    def __init__(self, id, name, time = 0, temperature = 0, humidity = 0):
        self.time = time
        self.temperature = temperature
        self.humidity = humidity
        super().__init__(id, name)

    '''
    Returns : objects main reading, in this case tempreture
    '''
    def getReading(self):
        return self.temperature
    
    '''
    Converts object to string

    return: string representaion of object
    '''
    def toStringFormat(self):
        return "(Name: " + str(self.name) + " ID: " + str(self.id) + " Temp: " + str(self.temperature) + " Time: " + str(self.time) + ") "
