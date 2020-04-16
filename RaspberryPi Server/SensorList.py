def Singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

@Singleton
class SensorList(object):

    def __init__(self):
        print("Init Singleton Sensor List Object")