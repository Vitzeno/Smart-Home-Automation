import bluetooth
import subprocess

class BluetoothHandler:
    # Bluetooth socket attributes
    server_sock = []
    client_sock = []
    client_info = []

    # Multiprocessing synchronisation
    MessageEvent = []
    SendEvent = []
    EndEvent = []
    ConnectEvent = []
    Dict = []
    Lock = []

    @classmethod
    def connectBT(cls, Dict, MessageEvent, EndEvent, ConnectEvent, SendEvent, lock):
        BluetoothHandler.Lock = lock
        BluetoothHandler.MessageEvent = MessageEvent
        BluetoothHandler.SendEvent = SendEvent
        BluetoothHandler.EndEvent = EndEvent
        BluetoothHandler.Dict = Dict
        BluetoothHandler.ConnectEvent = ConnectEvent

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
        BluetoothHandler.ConnectEvent.set()
        BluetoothHandler.Dict["name"] = BluetoothHandler.client_info[0]

        BluetoothHandler.startCommunication()
    
    @classmethod
    def startCommunication(cls):
        print("Communination Running...")
        while True:
            try:
                BluetoothHandler.Lock.acquire()
                BluetoothHandler.Dict["recv"] = BluetoothHandler.client_sock.recv(1024)
                
                data = BluetoothHandler.Dict["recv"].decode("utf-8")
                #print("Data = ", data)
                #BluetoothHandler.sendToClient(data)

                BluetoothHandler.MessageEvent.set()
                BluetoothHandler.Lock.release()

                BluetoothHandler.SendEvent.wait(0.25)

                if BluetoothHandler.SendEvent.is_set():
                    BluetoothHandler.sendToClient(BluetoothHandler.Dict["write"].encode("utf-8"))
                    BluetoothHandler.SendEvent.clear()

                if BluetoothHandler.EndEvent.is_set():
                    BluetoothHandler.cleanUpBT()
                    BluetoothHandler.EndEvent.clear()
                    break
                    
            except (OSError, KeyboardInterrupt) as e:
                BluetoothHandler.cleanUpBT()
                BluetoothHandler.EndEvent.clear()
                break

    @classmethod
    def sendToClient(cls, message):
        BluetoothHandler.client_sock.send(message)
        print("============================================================================")
        print("SENDING: ", message) 
        print("============================================================================")

    @classmethod
    def cleanUpBT(cls):
        BluetoothHandler.client_sock.close()
        BluetoothHandler.server_sock.close()