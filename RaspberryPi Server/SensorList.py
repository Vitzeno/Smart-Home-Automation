import requests 
import json
from datetime import datetime
import Serialise as Serialise
from Sensor import Sensor
from TimeSensor import TimeSensor


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
        print("Init Singleton Sensor List Object")
        self.sensorList = sensors
        self.counter = 0

    '''
    Adds a new senor to sensor list

    name: sensor name
    time: current time
    temperature: current temperature
    humidity: current humidity
    '''
    def addSensor(self, name, time = 0, temperature = 0, humidity = 0):
        print("Adding new sensor! ", name)
        self.counter += 1
        sensor = Sensor(self.counter, name, time, temperature, humidity)
        self.sensorList.append(sensor)
    
    '''
    Adds the default time senesor to sensor list

    name: name of sensor
    '''
    def addTimeSensor(self, name):
        time = TimeSensor(0, name)
        self.sensorList.append(time)

    '''    
    Since the constructor cannot be called agiain in a singleton, this method sets up the default

    This method requires a connection to the emonHub server to function, must wrap in try catch block
    '''
    def setUpDefaultData(self):
        print("Add default sensor data to object")
        self.addTimeSensor("Time")
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
    Update tempreture for each sensor in senor list when called

    This method requires a connection to the emonHub server to function, must wrap in try catch block
    '''
    def updateSensors(self):
        print("Updating tempreture and time")
        try:
            sensors = self.requestAllData()
            values = list(sensors.values())
            '''
            print(values)
            print(type(values))
            print(list(values[0]))
            print(list(values[0])[1])
            print(values[0][1])
            '''

            for i in range(0, len(values)):
                #if i == 0:
                    #continue
                self.sensorList[i+1].time = values[i][0]
                self.sensorList[i+1].temperature = values[i][1]
                self.sensorList[i+1].humidity = values[i][2]

            self.setSensorObject()
        except(IOError, OSError, FileNotFoundError, ValueError, KeyError, IndexError) as e:
            print("Failed to update sensors, make sure emonHub is running")


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

    return: deserialised object or newly created deivce list object
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
    
    '''
    Converts object to string

    return: string format of object
    '''
    def toStringFormat(self):
        allSensors = ""
        for i in self.sensorList:
            allSensors = allSensors + i.toStringFormat()
        return allSensors
    
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
            
    '''
    Uses a get request to return a dictionrry contaning sensor data from emonHub service
    '''
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
            HumidityData = currSensor["humidity"]
            time = TemperatureData["time"]   
            data.update({sensor : (time, TemperatureData["value"], HumidityData["value"])})
         
        return data
