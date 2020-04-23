import requests 
import json
from datetime import datetime
import Serialise as Serialise
from Sensor import Sensor


def Singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

@Singleton
class SensorList(object):
    
    sensorList = []
    FILE_DIR = "config/"
    FILE_TYPE = ".txt"
    FILE_NAME = "SensorList"

    def __init__(self, sensors = []):
        print("Init Singleton Device List Object")
        self.sensorList = sensors
        self.counter = 0

    def addSensor(self, name, time = 0, temperature = 0, humidity = 0):
        print("Adding new sensor! ", name)
        self.counter += 1
        sensor = Sensor(self.counter, name, time, temperature, humidity)
        self.sensorList.append(sensor)

    '''    
    Since the constructor cannot be called agiain in a singleton, this method sets up the default

    This method requires a connection to the emonHub server to function, must wrap in try catch block
    '''
    def setUpDefaultData(self):
        print("Add default sensor data to object")
        try:
            sensors = self.requestAllData()
            
            i = 0
            for sensor in sensors:
                data = sensors[sensor]
                self.addSensor(sensor, data[0], data[1], data[2])
                print("Adding sensor ", sensor)
                i +=1
                
            self.counter = i
        except (IOError, OSError, FileNotFoundError) as e:
            self.addSensor("sensor")


    '''
    Init the sensor list JSON file and write to disk, default parameters are used
    '''
    def initSensorList(self):
        print("Init sensor list and write to file")
        try:
            self.setUpDefaultData()
            Serialise.serialiseObjectToFile(self, self.FILE_NAME, self.FILE_DIR)
        except (IOError, OSError, FileNotFoundError) as e:
            print("Failed to init {0}" .format(self.FILE_NAME))
    
    '''
    Read sensor list from disk, if it does not exist call init to create one with default parameters

    Use this method to access the sensor list object
    '''
    def getSensorObject(self):
        try:
            slObject = Serialise.deserialiseObjectFromFile(self.FILE_NAME, self.FILE_DIR)
        except (IOError, OSError, FileNotFoundError) as e:
            print("File {0} not found, init default data" .format(self.FILE_NAME))
            self.initSensorList()
        
        slObject = Serialise.deserialiseObjectFromFile(self.FILE_NAME, self.FILE_DIR)
        return slObject
    
    
    '''
    Write object to file
    '''
    def setSensorObject(self):
        try:
            Serialise.serialiseObjectToFile(self, self.FILE_NAME, self.FILE_DIR)
        except (IOError, OSError, FileNotFoundError) as e:
            print("Failed to write new object {0} to file" .format(self.FILE_NAME))
    
    def toStringFormat(self):
        for i in self.sensorList:
            print(i.toStringFormat())
    
    '''
    Search for a sensor object by ID, possible that ID and list index are the same

    If it fails it will raise a ValueError exception
    '''
    def getSensorByID(self, id):
        if int(id) > int(self.counter):
            raise ValueError("ID not in range")
        for sensor in self.sensorList:
            if int(sensor.id) == int(id):
                return sensor
        
        raise ValueError("ID not found in list")
            

    def requestAllData(self):
        with requests.Session() as session:
            session.auth = ('TheGrind', 'TheGrind')
            r = session.get('http://192.168.0.26/input/get&apikey=b7fafeb753e6fde29dd957c494bb1763')

            if r:
                print("Fetched data...")

        #print(r.encoding)
        #print(r.status_code)
        js = r.json()
        #print("Parsing")
        #print("json = ", js)
        data = dict()
        
        #print("length = ", len(js))
        #print("list = ", list(js))
        
        for sensor in js:
            currSensor = js[sensor]
            TemperatureData = currSensor["temperature"]
            #print("Temperature¬ Time: ", datetime.fromtimestamp(TemperatureData["time"]), "Value: ", TemperatureData["value"]) 
            HumidityData = currSensor["humidity"]
            #print("Humidity¬ Time:", datetime.fromtimestamp(HumidityData["time"]), "Value: ", HumidityData["value"])
            time = TemperatureData["time"]   
            data.update({sensor : (time, TemperatureData["value"], HumidityData["value"])})
         
        return data
