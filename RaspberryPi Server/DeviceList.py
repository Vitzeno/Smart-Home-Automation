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

    def __init__(self, devices = []):
        print("Init Singleton Device List Object")
        self.devicesList = devices
    
    def addDevice(self, device):
        self.devicesList.append(device)

    def addDevices(self, devices):
        self.devicesList.extend(devices)

