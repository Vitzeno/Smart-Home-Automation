from Devices import Devices

class Group(object):
    
    def __init__(self, name, devices = []):
        self.devices = devices
    
    def addDevice(self, device):
        self.devices.append(device)
    
    def addDevices(self, devices):
        self.devices.extend(devices)
    
    def switchAll(self, state):
        for device in self.devices:
            device.switchDevice(state)
        
    def printAll(self):
        for device in self.devices:
            print(device.toString())