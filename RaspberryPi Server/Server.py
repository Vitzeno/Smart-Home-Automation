from multiprocessing import Process, Manager, Lock, Event
from json import JSONEncoder
import bluetooth
import RPi.GPIO as GPIO
import time
import subprocess
import json
import jsonpickle
import os

import Radio as Radio
import Serialise as Serialise
from BluetoothHandler import BluetoothHandler
from Devices import Devices
from DeviceList import DeviceList
from Parser import Parser
from Expression import Expression
from Rule import Rule
from Sensor import Sensor
from SensorList import SensorList
from Group import Group
from GroupList import GroupList

running = []

def comms():
    dictionary = Manager().dict()
    dictionary["recv"] = []
    dictionary["write"] = []
    dictionary["name"] = []
    dictionary["status"] = []
    lock = Lock()
    MessageEvent = Event()
    SendEvent = Event()
    EndEvent = Event()
    ConnectEvent = Event()
  
    proc = Process(target = BluetoothHandler.connectBT, args = (dictionary, MessageEvent, EndEvent, ConnectEvent, SendEvent, lock))
    proc.start()
    switch = True                           ##hack for second obj, remove

    print(subprocess.getoutput("hcitool con").split())

    ConnectEvent.wait()
    conStatus = True
    #print(type(dictionary["status"]))
    try:
        while conStatus: #dictionary["status"]:

            print(dictionary["name"])
            print(subprocess.getoutput("hcitool con").split())
            MessageEvent.wait(2)
            
            status = subprocess.getoutput("hcitool con").split()
            
            if not (len(status) > 3 and status[3] == dictionary["name"]):
                conStatus = False

            if MessageEvent.is_set():
                print(dictionary["recv"].decode("utf-8"))

                if(dictionary["recv"].decode("utf-8") == 'H'):
                    Radio.switchSocket(1, True)
                if(dictionary["recv"].decode("utf-8") == 'L'):
                    Radio.switchSocket(1, False)
                
                if(dictionary["recv"].decode("utf-8") == 'S'):
                    switch = not switch
                    Radio.switchSocket(2, switch)
                pass
            MessageEvent.clear()
    except (OSError, KeyboardInterrupt) as e:
        EndEvent.set()
        ConnectEvent.clear()
        proc.join()
        Radio.cleanUp()
        running = False
    
    Radio.cleanUp()
    EndEvent.set()
    ConnectEvent.clear()
    print("Waiting to join")
    proc.join()
    Radio.cleanUp()

if __name__ == '__main__':
    Radio.setUp()
    Serialise.setDirectory()

    '''
    s1 = Sensor(0, "Temp")
    s2 = Sensor(1, "Humid")

    list1 = [Expression().equalsTo(s1, 12), Expression().greaterThan(s2, 0), "AND", Expression().equalsTo(s1, 12), Expression().lessThan(s2, 3), "OR", Expression().equalsTo(s1, 12), Expression().lessThan(s2, 3), "OR", "OR", "AND"]
    r1 = Rule()
    r1.evaluate(list1)

    list2 = [Expression().equalsTo(s1, 22), Expression().greaterThan(s2, 0), "AND"]
    r2 = Rule()
    r2.evaluate(list2)

    group1 = Serialise.deserialiseObjectFromFile("Groups")
    group1.printAll()
    group1.switchAll(True)
    '''
    sL = SensorList()
    dL = DeviceList()
    gL = GroupList()

    d1 = Devices(1, "Lamp")
    d2 = Devices(2, "Washer")
    d3 = Devices(3, "TV")
    d4 = Devices(4, "Computer")

    g1 = Group("Group 2")
    g1.addDevice(d1)
    g1.addDevice(d2)

    g2 = Group("Group 2")
    g2.addDevice(d3)
    g2.addDevice(d4)

    gL.addGroup(g1)
    gL.addGroup(g2)

    dL.addDevice(d1)
    dL.addDevice(d2)

    Serialise.serialiseObjectToFile(dL, "DeviceList")
    Serialise.serialiseObjectToFile(gL, "GroupList")

    p = Parser()
    # valid commands
    p.parseInput("C:G:C:Group 1:3:2:1")
    p.parseInput("C:G:D:Group 1")
    p.parseInput("C:D:E:2:Test")
    p.parseInput("C:D:S:2:1")
    p.parseInput("C:G:S:3:0")
    
    running = True
    while running:
        comms()
    Radio.cleanUp()
    print("Gracefully Quit")