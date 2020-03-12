from multiprocessing import Process, Manager, Lock, Event
import bluetooth
import RPi.GPIO as GPIO
import time
import subprocess

import Radio as radio
import BluetoothHandler as BTHandler

if __name__ == '__main__':
    radio.setUp()

    with Manager() as manager:
        dictionary = manager.dict()
        lock = Lock()
        MessageEvent = Event()
        EndEvent = Event()

        proc = Process(target = BTHandler.BluetoothHandler.connectBT, args = (dictionary, MessageEvent, EndEvent, lock))
        proc.start()
        switch = True

        try:
            while True:
                MessageEvent.wait(5)

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
            radio.cleanUp()
        
        print("Waiting to join")
        proc.join()
        radio.cleanUp()
        print("Gracefully Quit")