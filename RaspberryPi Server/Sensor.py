from Devices import Devices

class Sensor(Devices):

    def __init__(self, id, name, lastKnownState = 0, reading = 0):
        self.reading = reading
        super().__init__(id, name, lastKnownState)
    
    def toString(self):
        return "Name: " + self.name + " ID: " + str(self.id) + " State: " + str(self.lastKnownState) + " Reading: " + str(self.reading)
