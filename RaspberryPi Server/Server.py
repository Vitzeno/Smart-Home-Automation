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
from ParserException import ParserException
from Expression import Expression
from RuleEvaluator import RuleEvaluator
from RuleList import RuleList
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

    deviceList = DeviceList().getDevicesObject()
    print(deviceList.toStringFormat())

    groupList = GroupList().getGroupObject()
    print(groupList.toStringFormat())

    sensorList = SensorList().getSensorObject()
    print(sensorList.toStringFormat())
    
    ruleList = RuleList().getRuleObject()
    print(ruleList.toStringFormat())

    s1 = sensorList.getSensorByID(1)
    s2 = sensorList.getSensorByID(2)
    #ruleList.createRule("New Rule", [Expression().equalsTo(s1, 22), Expression().greaterThan(s2, 0), "AND"])
    #ruleList.setRuleObject()

    try:
        print(groupList.getGroupByID(4).toStringFormat())
    except (ValueError) as e:
        print(e)
    
    try:
        print(sensorList.getSensorByID(2).toStringFormat())
    except (ValueError) as e:
        print(e)
    
    try:
        print(ruleList.getRuleByID(3).toStringFormat())
    except (ValueError) as e:
        print(e)

    p = Parser()
    # valid commands

    p.parseInput("R:S:2")
    p.parseInput("R:R:4")
    p.parseInput("R:D:7")
    p.parseInput("R:G:6")
    p.parseInput("R:AS")
    p.parseInput("R:AR")
    p.parseInput("R:AD")
    p.parseInput("R:AG")

    try:
        p.parseInput("C:R:C:f:OR:e:AND:EQ:LE")
    except (ParserException) as e:
        print(e)
        
    try:
        p.parseInput("C:R:C:21:GE:LE:AND")
    except (ParserException) as e:
        print(e)

    try:
        p.parseInput("C:R:C:21::GE:LE:AND")
    except (ParserException) as e:
        print(e)

    
    running = True
    while running:
        comms()
    Radio.cleanUp()
    print("Gracefully Quit")