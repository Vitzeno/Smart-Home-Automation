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
        self.counter = 0
    
    '''
    Adds a new deivces to the devices list and auto increments ID

    Name: name of device
    '''
    def addDevice(self, name):
        self.counter += 1
        device = Devices(self.counter, name)
        self.devicesList.append(device)

    '''
    Since the constructor cannot be called agiain in a singleton, this method sets up the default
    '''
    def setUpDefaultData(self):
        print("Add default data to object")
        self.addDevice("Device_One")
        self.addDevice("Device_Two")
        self.addDevice("Device_Three")
        self.addDevice("Device_Four")
        self.counter = 4

    '''
    Init the device list JSON file and write to disk, default parameters are used
    '''
    def initDeviceList(self):
        print("Init devices list and write to file")
        try:
            self.setUpDefaultData()
            Serialise.serialiseObjectToFile(self, self.FILE_NAME, self.FILE_DIR)
        except (IOError, OSError, FileNotFoundError) as e:
            print("Failed to init {0}" .format(self.FILE_NAME))
    
    '''
    Read device list from disk, if it does not exist call init to create one with default parameters

    Use this method to access the devices list object

    return: deserialised object or newly created deivce list object
    '''
    def getDevicesObject(self):
        try:
            dlObject = Serialise.deserialiseObjectFromFile(self.FILE_NAME, self.FILE_DIR)
        except (IOError, OSError, FileNotFoundError) as e:
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
        except (IOError, OSError, FileNotFoundError) as e:
            print("Failed to write new object {0} to file" .format(self.FILE_NAME))

        '''
    Search for a device object by ID, possible that ID and list index are the same

    If it fails it will raise a ValueError exception
    '''
    def getDeviceByID(self, id):
        if int(id) > int(self.counter):
            raise ValueError("ID not in range")
        for device in self.devicesList:
            if int(device.id) == int(id):
                return device
        
        raise ValueError("ID not found in list")
    
    '''
    Converts object to sting

    return: String format of object
    '''
    def toStringFormat(self):
        allDevice = ""
        for i in self.devicesList:
            allDevice = allDevice + i.toStringFormat()
        return allDevice
            


