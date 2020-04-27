from Devices import Devices
from datetime import datetime

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
        now = datetime.now()
        seconds_since_midnight = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
        minutes_since_midnigth = seconds_since_midnight / 60
        self.time = round(minutes_since_midnigth)
        return self.time
    
    '''
    Converts object to string

    return: string representaion of object
    '''
    def toStringFormat(self):
        return "{Name: " + str(self.name) + " ID: " + str(self.id) + " Time: " + str(self.time) + "} "