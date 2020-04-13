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
from Parser import Parser
from Expression import Expression
from Rule import Rule
from Sensor import Sensor
from Group import Group

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

    p = Parser()
    # valid commands
    p.parseInput("C:R:C:S1:21:GE:S2:12:LE:AND")

    running = True
    while running:
        comms()
    Radio.cleanUp()
    print("Gracefully Quit")