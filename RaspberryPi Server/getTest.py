import requests 
import json
from datetime import datetime

def requestData():
    with requests.Session() as session:
        session.auth = ('TheGrind', 'TheGrind')
        r = session.get('http://192.168.0.26/input/get&apikey=b7fafeb753e6fde29dd957c494bb1763')

        if r:
            print("Fetched something...")

    print(r.encoding)
    print(r.status_code)

    js = r.json()
    print("Parsing")
    #print("json = ", js)
    sensors = dict()
    
    print("length = ", len(js))
    print("list = ", list(js))
    
    i = 0
    for sensor in js:
        name = sensor
        
        currSensor = js[name]
        TemperatureData = currSensor["temperature"]
        print("Temperature¬ Time: ", datetime.fromtimestamp(TemperatureData["time"]), "Value: ", TemperatureData["value"]) 
        HumidityData = currSensor["humidity"]
        print("Humidity¬ Time:", datetime.fromtimestamp(HumidityData["time"]), "Value: ", HumidityData["value"])
        
        time = TemperatureData["time"]
        
        sensors.update({name : (time, TemperatureData["value"], HumidityData["value"])})
        
        i += 1
    
    return sensors


data = requestData()
print(data)