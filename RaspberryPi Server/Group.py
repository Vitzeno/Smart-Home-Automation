from Devices import Devices

class Group(object):

    devices = []
    
    def __init__(self, id, name, devices = []):
        self.id = id
        self.name = name
        self.devices = devices
    
    def addDevice(self, device):
        self.devices.append(device)
    
    def addDevices(self, devices):
        self.devices.extend(devices)
    
    def switchAll(self, state):
        for device in self.devices:
            device.switchDevice(state)
    
    def toStringFormat(self):
        return "Name: " + str(self.name) + " ID: " + str(self.id) + " Devices: " + str(self.devices)
        
    def printAllDevices(self):
        for device in self.devices:
            print(device.toString())