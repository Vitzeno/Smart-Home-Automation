from Group import Group

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

    def __init__(self, groups = []):
        print("Init Singleton Group List Object")
        self.groupList = groups
    
    def addGroup(self, group):
        self.groupList.append(group)

    def addGroups(self, groups):
        self.groupList.extend(groups)