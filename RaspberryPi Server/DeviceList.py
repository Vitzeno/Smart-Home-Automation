import Serialise as Serialise
from Devices import Devices

def Singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

@Singleton
class DeviceList(object):

    devicesList = []
    FILE_DIR = "config/"
    FILE_TYPE = ".txt"
    FILE_NAME = "DeviceList"

    def __init__(self, devices = []):
        print("Init Singleton Device List Object")
        self.devicesList = devices
    
    def addDevice(self, device):
        self.devicesList.append(device)

    def addDevices(self, devices):
        self.devicesList.extend(devices)

    '''
    Since the constructor cannot be called agiain in a singleton, this method sets up the default
    '''
    def setUpDefaultData(self):
        print("Add default data to object")
        d1 = Devices(1, "Device One")
        d2 = Devices(2, "Device Two")
        d3 = Devices(3, "Device Three")
        d4 = Devices(4, "Device Four")
        self.addDevice(d1)
        self.addDevice(d2)
        self.addDevice(d3)
        self.addDevice(d4)

    '''
    Init the device list JSON file and write to disk, default parameters are used
    '''
    def initDeviceList(self):
        print("Init devices list and write to file")
        try:
            self.setUpDefaultData()
            Serialise.serialiseObjectToFile(self, self.FILE_NAME, self.FILE_DIR)
        except (IOError, OSError) as e:
            print("Failed to init {0}" .format(self.FILE_NAME))
    
    '''
    Read device list from disk, if it does not exist call init to create one with default parameters
    '''
    def getDevicesObject(self):
        try:
            dlObject = Serialise.deserialiseObjectFromFile(self.FILE_NAME, self.FILE_DIR)
        except (IOError, OSError) as e:
            print("File {0} not found, init default data" .format(self.FILE_NAME))
            self.initDeviceList()
        
        dlObject = Serialise.deserialiseObjectFromFile(self.FILE_NAME, self.FILE_DIR)
        return dlObject

    '''
    Write object to file
    '''
    def setDevicesObject(self):
        try:
            Serialise.serialiseObjectToFile(self, self.FILE_NAME, self.FILE_DIR)
        except (IOError, OSError) as e:
            print("Failed to write new object {0} to file" .format(self.FILE_NAME))
    
    def toStringFormat(self):
        for i in self.devicesList:
            print(i.toStringFormat())
            


