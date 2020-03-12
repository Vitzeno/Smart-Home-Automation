from multiprocessing import Process, Manager, Lock, Event
import bluetooth
import RPi.GPIO as GPIO
import time
import subprocess

import Radio as radio
import BluetoothHandler as BTHandler

running = []

def comms():
    radio.setUp()
    dictionary = Manager().dict()
    dictionary["recv"] = []
    dictionary["name"] = []
    dictionary["status"] = []
    lock = Lock()
    MessageEvent = Event()
    EndEvent = Event()
    ConnectEvent = Event()
  
    proc = Process(target = BTHandler.BluetoothHandler.connectBT, args = (dictionary, MessageEvent, EndEvent, ConnectEvent, lock))
    proc.start()
    switch = True                           ##hack for second obj, remove

    print(subprocess.getoutput("hcitool con").split())
    print("Waiting for connection")

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
                    radio.switchSocket(1, True)
                if(dictionary["recv"].decode("utf-8") == 'L'):
                    radio.switchSocket(1, False)
                
                if(dictionary["recv"].decode("utf-8") == 'S'):
                    switch = not switch
                    radio.switchSocket(2, switch)
                pass
            MessageEvent.clear()
    except (OSError, KeyboardInterrupt) as e:
        EndEvent.set()
        ConnectEvent.clear()
        proc.join()
        radio.cleanUp()
        running = False
    
    radio.cleanUp()
    EndEvent.set()
    ConnectEvent.clear()
    print("Waiting to join")
    proc.join()
    radio.cleanUp()

if __name__ == '__main__':

    running = True
    while running:
        comms()
    radio.cleanUp()
    print("Gracefully Quit")