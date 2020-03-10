from multiprocessing import Process, Manager, Lock, Event
import bluetooth
import RPi.GPIO as GPIO
import time
import subprocess

import Radio as radio

class BluetoothHandler:

    server_sock = []
    client_sock = []
    client_info = []
    
    @classmethod
    def __init__(cls):
        print("Constructor CS: ", BluetoothHandler.client_sock, " SS: ", BluetoothHandler.server_sock)

    @classmethod
    def connectBT(cls, dict, event, lock):
        print("pre-connectBT CS: ", BluetoothHandler.client_sock, " SS: ", BluetoothHandler.server_sock)
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

        lock.acquire()
        dict["test"] = 5
        event.set()
        lock.release()
        print("post-connectBT CS: ", BluetoothHandler.client_sock, " SS: ", BluetoothHandler.server_sock)

    @classmethod
    def cleanUpBT(cls):
        print("cleanUp CS: ", BluetoothHandler.client_sock, " SS: ", BluetoothHandler.server_sock)
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
        event = Event()

        proc = Process(target = BluetoothHandler.connectBT, args = (dictionary, event, lock))
        proc.start()

        try:
            while True:
                event.wait(5)
                if event.is_set():
                    print(dictionary)
                event.clear()
        except (OSError, KeyboardInterrupt) as e:
            radio.cleanUp()
            pass

        proc.join()

        BluetoothHandler.cleanUpBT()
        radio.cleanUp()