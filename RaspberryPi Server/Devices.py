import Radio as Radio

class Devices(object):

    def __init__(self, id, name, lastKnownState = 0):
        self.id = id
        self.name = name
        self.lastKnownState = lastKnownState
    
    def switchDevice(self, state):
        Radio.switchSocket(self.id, state)
    
    def toStringFormat(self):
        return "Name: " + self.name + " ID: " + str(self.id) + " State: " + str(self.lastKnownState)
        