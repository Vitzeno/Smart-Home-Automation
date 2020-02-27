from multiprocessing import Process, Manager, Lock, Event
import bluetooth
import RPi.GPIO as GPIO
import time
import subprocess

import Radio as radio

class BluetoothHandler:
    
    def __init__(self):
        self.server_sock = BluetoothHandler
        self.client_sock = BluetoothHandler
        self.client_info = BluetoothHandler
        print("Constructor CS: ", self.client_sock, " SS: ", self.server_sock)

    def connectBT(self, dict, event, lock):
        print("pre-connectBT CS: ", self.client_sock, " SS: ", self.server_sock)
        # setup bt connection
        self.server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.server_sock.bind(("", bluetooth.PORT_ANY))
        self.server_sock.listen(1)

        port = self.server_sock.getsockname()[1]
        
        uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

        bluetooth.advertise_service(self.server_sock, "SampleServer", service_id=uuid,
                                    service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                                    profiles=[bluetooth.SERIAL_PORT_PROFILE],
                                    # protocols=[bluetooth.OBEX_UUID]
                                    )

        print("Waiting for connection on RFCOMM channel", port)
        self.client_sock, self.client_info = self.server_sock.accept()
        print("Accepted connection from", self.client_info)

        lock.acquire()
        dict["test"] = 5
        event.set()
        lock.release()
        print("post-connectBT CS: ", self.client_sock, " SS: ", self.server_sock)

    def cleanUpBT(self):
        print("cleanUp CS: ", self.client_sock, " SS: ", self.server_sock)
        self.client_sock.close()
        self.server_sock.close()

    def close():
        print("Close")

if __name__ == '__main__':
    radio.setUp()

    with Manager() as manager:
        dictionary = manager.dict()
        lock = Lock()
        event = Event()

        BTHandler = BluetoothHandler()

        proc = Process(target = BTHandler.connectBT, args = (dictionary, event, lock))
        proc.start()

        try:
            while True:
                event.wait(5)
                if event.is_set():
                    print(dictionary)
                    print("External CS: ", BTHandler.client_sock, " SS: ", BTHandler.server_sock)
                event.clear()
        except (OSError, KeyboardInterrupt) as e:
            radio.cleanUp()
            pass

        proc.join()

        BTHandler.cleanUpBT()
        radio.cleanUp()