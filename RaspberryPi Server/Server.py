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

running = []

def comms():
    Radio.setUp()
    dictionary = Manager().dict()
    dictionary["recv"] = []
    dictionary["name"] = []
    dictionary["status"] = []
    lock = Lock()
    MessageEvent = Event()
    EndEvent = Event()
    ConnectEvent = Event()
  
    proc = Process(target = BluetoothHandler.connectBT, args = (dictionary, MessageEvent, EndEvent, ConnectEvent, lock))
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
    Serialise.setDirectory()

    p = Parser()
    # valid commands
    p.parseInput("CG30")
    p.parseInput("CD21")
    p.parseInput("CRC1")
    p.parseInput("CRE21")
    p.parseInput("CRD2")
    p.parseInput("RS3")
    p.parseInput("RA")
    # invalid commands
    p.parseInput("F30")
    p.parseInput("sgs")
    p.parseInput("34tsd")
    p.parseInput("CR3e")
    # false positve commands
    p.parseInput("RS3sdfwet")
    p.parseInput("CRD23454336")

    running = True
    while running:
        comms()
    Radio.cleanUp()
    print("Gracefully Quit")