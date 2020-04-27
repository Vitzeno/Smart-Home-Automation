import Radio as Radio

class Devices(object):

    def __init__(self, id, name, lastKnownState = 0):
        self.id = id
        self.name = name
        self.lastKnownState = lastKnownState
    
    '''
    Uses RF to switch a device on or off
    
    state: new state of deivce
    '''
    def switchDevice(self, state):
        Radio.switchSocket(self.id, state)
    
    '''
    Convers deivice into a string

    return: string representaion of device
    '''
    def toStringFormat(self):
        return "(Name: " + str(self.name) + " ID: " + str(self.id) + " State: " + str(self.lastKnownState) + ") "
        