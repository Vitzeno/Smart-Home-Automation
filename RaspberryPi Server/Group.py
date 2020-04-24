from Devices import Devices

class Group(object):

    devices = []
    
    def __init__(self, id, name, devices = []):
        self.id = id
        self.name = name
        self.devices = devices
    
    '''
    Adds a device to a group

    deivce: device object to add
    '''
    def addDevice(self, device):
        self.devices.append(device)
    
    '''
    Adds a list of deivces to a group

    devices: list of devices to add
    '''
    def addDevices(self, devices):
        self.devices.extend(devices)
    
    '''
    Switch all deives in this group to a given state using eacg devices switch methis

    state: state to switch to
    '''
    def switchAll(self, state):
        for device in self.devices:
            device.switchDevice(state)
    
    '''
    Convets object into string

    return: string represntation of object
    '''
    def toStringFormat(self):
        return "Name: " + str(self.name) + " ID: " + str(self.id) + " Devices: " + str(self.devices)
    
    '''
    Prints all devicecs in a group to console [DEBUG]
    '''
    def printAllDevices(self):
        for device in self.devices:
            print(device.toString())