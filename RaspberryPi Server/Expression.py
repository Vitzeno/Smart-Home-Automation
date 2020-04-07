class Expression:

    def __init__(self, sensorObject, reading):
        self.sensorObject = sensorObject
        self.reading = reading

    def equalsTo(self):
        if self.sensorObject.reading == self.reading:
            return True
        return False
    
    def greaterThan(self):
        if self.sensorObject.reading > self.reading:
            return True
        return False
    
    def lessThan(self):
        if self.sensorObject.reading < self.reading:
            return True
        return False