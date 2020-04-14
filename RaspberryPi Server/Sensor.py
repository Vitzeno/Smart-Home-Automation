from Devices import Devices

class Sensor(Devices):

    def __init__(self, id, name, lastKnownState = 0, reading = 0, time = 0):
        self.reading = reading
        super().__init__(id, name, lastKnownState)
    
    def setTime(self, time):
        self.time = time
    
    def setReading(self, reading):
        self.reading = reading

    def getTime(self):
        return self.time

    def getReading(self):
        return self.reading
 
    def toString(self):
        return "Name: " + self.name + " ID: " + str(self.id) + " State: " + str(self.lastKnownState) + " Reading: " + str(self.reading) + " Time: " + str(self.time)
