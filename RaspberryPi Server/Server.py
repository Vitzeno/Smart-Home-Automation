from multiprocessing import Process, Manager, Lock, Event
import bluetooth
import RPi.GPIO as GPIO
import time
import subprocess

import Radio as radio

class BluetoothHandler:
    # Bluetooth socket attributes
    server_sock = []
    client_sock = []
    client_info = []

    # Multiprocessing synchronisation
    MessageEvent = []
    EndEvent = []
    Dict = []
    Lock = []

    @classmethod
    def __init__(cls):
        print("Constructor CS: ", BluetoothHandler.client_sock, " SS: ", BluetoothHandler.server_sock)

    @classmethod
    def connectBT(cls, Dict, MessageEvent, EndEvent, lock):
        #print("pre-connectBT CS: ", BluetoothHandler.client_sock, " SS: ", BluetoothHandler.server_sock)
        # setup bt connection
        BluetoothHandler.server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        BluetoothHandler.server_sock.bind(("", bluetooth.PORT_ANY))
        BluetoothHandler.server_sock.listen(1)

        port = BluetoothHandler.server_sock.getsockname()[1]
        
        uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

        bluetooth.advertise_service(BluetoothHandler.server_sock, "SampleServer", service_id=uuid,
                                    service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                                    profiles=[bluetooth.SERIAL_PORT_PROFILE],
                                    # protocols=[bluetooth.OBEX_UUID]
                                    )

        print("Waiting for connection on RFCOMM channel", port)
        BluetoothHandler.client_sock, BluetoothHandler.client_info = BluetoothHandler.server_sock.accept()
        print("Accepted connection from", BluetoothHandler.client_info)

        BluetoothHandler.Lock = lock
        BluetoothHandler.MessageEvent = MessageEvent
        BluetoothHandler.EndEvent = EndEvent
        BluetoothHandler.Dict = Dict

        #print("post-connectBT CS: ", BluetoothHandler.client_sock, " SS: ", BluetoothHandler.server_sock)
        BluetoothHandler.startCommunication()
    
    @classmethod
    def startCommunication(cls):
        while True:
            try:
                BluetoothHandler.Lock.acquire()
                BluetoothHandler.Dict["recv"] = BluetoothHandler.client_sock.recv(1024)
                BluetoothHandler.MessageEvent.set()
                BluetoothHandler.Lock.release()

                if BluetoothHandler.EndEvent.is_set():
                    BluetoothHandler.cleanUpBT()
                    BluetoothHandler.EndEvent.clear()
                    break
            except (OSError, KeyboardInterrupt) as e:
                BluetoothHandler.cleanUpBT()
                BluetoothHandler.EndEvent.clear()
                break
                

    @classmethod
    def cleanUpBT(cls):
        #print("cleanUp CS: ", BluetoothHandler.client_sock, " SS: ", BluetoothHandler.server_sock)
        BluetoothHandler.client_sock.close()
        BluetoothHandler.server_sock.close()

    @classmethod
    def close(cls):
        print("Close")

if __name__ == '__main__':
    radio.setUp()

    with Manager() as manager:
        dictionary = manager.dict()
        lock = Lock()
        MessageEvent = Event()
        EndEvent = Event()

        proc = Process(target = BluetoothHandler.connectBT, args = (dictionary, MessageEvent, EndEvent, lock))
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