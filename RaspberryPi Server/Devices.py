class Devices(object):

    def __init__(self, id, name, lastKnownState = 0):
        self.id = id
        self.name = name
        self.lastKnownState = lastKnownState
    
    def toString(self):
        return "Name: " + self.name + " ID: " + str(self.id) + " State: " + str(self.lastKnownState)
        