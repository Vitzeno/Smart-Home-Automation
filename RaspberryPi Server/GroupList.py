from Group import Group
import Serialise as Serialise

def Singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

@Singleton
class GroupList(object):

    groupList = []
    FILE_DIR = "config/"
    FILE_TYPE = ".txt"
    FILE_NAME = "GroupList"

    def __init__(self, groups = []):
        print("Init Singleton Group List Object")
        self.groupList = groups
        self.counter = 0
    
    '''
    Creates a group of devices and auto increments ID
    '''
    def createGroup(self, name, devices):
        self.counter += 1
        group = Group(self.counter, name, devices)
        self.groupList.append(group)
    
    '''
    Since the constructor cannot be called agiain in a singleton, this method sets up the default
    '''
    def setUpDefaultData(self):
        print("Add default data to object")
        self.createGroup("Group One", [])
        self.createGroup("Group Two", [])
        self.createGroup("Group Three", [])
        self.createGroup("Group Four", [])
        self.counter = 4
    
    '''
    Init the device list JSON file and write to disk, default parameters are used
    '''
    def initGroupList(self):
        print("Init group list and write to file")
        try:
            self.setUpDefaultData()
            Serialise.serialiseObjectToFile(self, self.FILE_NAME, self.FILE_DIR)
        except (IOError, OSError, FileNotFoundError) as e:
            print("Failed to init {0}" .format(self.FILE_NAME))
    
    '''
    Read device list from disk, if it does not exist call init to create one with default parameters

    Use this method to access the devices list object
    '''
    def getGroupObject(self):
        try:
            glObject = Serialise.deserialiseObjectFromFile(self.FILE_NAME, self.FILE_DIR)
        except (IOError, OSError, FileNotFoundError) as e:
            print("File {0} not found, init default data" .format(self.FILE_NAME))
            self.initGroupList()
        
        glObject = Serialise.deserialiseObjectFromFile(self.FILE_NAME, self.FILE_DIR)
        return glObject

    '''
    Write object to file
    '''
    def setGroupObject(self):
        try:
            Serialise.serialiseObjectToFile(self, self.FILE_NAME, self.FILE_DIR)
        except (IOError, OSError, FileNotFoundError) as e:
            print("Failed to write new object {0} to file" .format(self.FILE_NAME))
    
    '''
    Prints out group data in string format
    '''
    def toStringFormat(self):
        for i in self.groupList:
            print(i.toStringFormat())

    '''
    Search for a group object by ID, possible that ID and list index are the same

    If it fails it will raise a ValueError exception
    '''
    def getGroupByID(self, id):
        if int(id) > int(self.counter):
            raise ValueError("ID not in range")
        for group in self.groupList:
            if int(group.id) == int(id):
                return group
        
        raise ValueError("ID not found in list")

