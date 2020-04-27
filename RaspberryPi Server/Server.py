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
from RuleHandler import RuleHandler
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
parser = Parser()

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

            #print(dictionary["name"])
            #print(subprocess.getoutput("hcitool con").split())
            MessageEvent.wait(0.25)
            
            status = subprocess.getoutput("hcitool con").split()
            
            if not (len(status) > 3 and status[3] == dictionary["name"]):
                conStatus = False

            if MessageEvent.is_set():
                print("\n Main Thread Recived: {0} \n" .format(dictionary["recv"].decode("utf-8")))
                try:
                    data = parser.parseInput(dictionary["recv"].decode("utf-8"))
                    if data is not None:
                        print(data)
                        dictionary["write"] = data
                        SendEvent.set()
                except (ParserException) as e:
                    print(e)
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
    #print(deviceList.toStringFormat())

    groupList = GroupList().getGroupObject()
    #print(groupList.toStringFormat())

    sensorList = SensorList().getSensorObject()
    #print(sensorList.toStringFormat())

    ruleList = RuleList().getRuleObject()
    #print(ruleList.toStringFormat())

    #eval = RuleEvaluator()
    #print("Server Evaluated to: {0}" .format(eval.parseRule(ruleList.getRuleByID(3).rule)))

    #parser.parseInput("C:R:C:3:0:1:LE")
    try:
        parser.parseInput("C:G:S:7:1")
    except (ParserException) as e:
        print(e)

    #print(parser.parseInput("R:AR"))
    #print(parser.parseInput("R:R:3"))
    #print(parser.parseInput("R:R:69"))

    proc = Process(target = RuleHandler.beginEvaluation)
    proc.start()
    
    running = True
    
    while running:
        comms()

    Radio.cleanUp()
    print("Gracefully Quit")