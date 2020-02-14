import bluetooth
import RPi.GPIO as GPIO
import time
import subprocess

# make bt discoverable
subprocess.call(['sudo', 'hciconfig', 'hci0', 'piscan'])

# set the pins numbering mode
GPIO.setmode(GPIO.BOARD)

# Select the GPIO pins used for the encoder K0-K3 data inputs
GPIO.setup(11, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)

# Select the signal to select ASK/FSK
GPIO.setup(18, GPIO.OUT)

# Select the signal used to enable/disable the modulator
GPIO.setup(22, GPIO.OUT)

# Disable the modulator by setting CE pin lo
GPIO.output (22, False)

# Set the modulator to ASK for On Off Keying 
# by setting MODSEL pin lo
GPIO.output (18, False)

# Initialise K0-K3 inputs of the encoder to 0000
GPIO.output (11, False)
GPIO.output (15, False)
GPIO.output (16, False)
GPIO.output (13, False)

# setup bt connection
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

bluetooth.advertise_service(server_sock, "SampleServer", service_id=uuid,
                            service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                            profiles=[bluetooth.SERIAL_PORT_PROFILE],
                            # protocols=[bluetooth.OBEX_UUID]
                            )

print("Waiting for connection on RFCOMM channel", port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from", client_info)

try:
    while True:
        data = client_sock.recv(1024)

        if not data:
            break
        print("Recived: ", data)

        if(data == 'H'):
            # Set K0-K3
            print "sending code 1111 socket 1 on"
            GPIO.output (11, True)
            GPIO.output (15, True)
            GPIO.output (16, True)
            GPIO.output (13, True)
            # let it settle, encoder requires this
            time.sleep(0.1) 
            # Enable the modulator
            GPIO.output (22, True)
            # keep enabled for a period
            time.sleep(0.25)
            # Disable the modulator
            GPIO.output (22, False)

        if(data == 'L'):
            print "sending code 0111 Socket 1 off"
            GPIO.output (11, True)
            GPIO.output (15, True)
            GPIO.output (16, True)
            GPIO.output (13, False)
            # let it settle, encoder requires this
            time.sleep(0.1)
            # Enable the modulator
            GPIO.output (22, True)
            # keep enabled for a period
            time.sleep(0.25)
            # Disable the modulator
            GPIO.output (22, False)
except (OSError, KeyboardInterrupt) as e:
    GPIO.cleanup()
    pass

print("Disconnected")

client_sock.close()
server_sock.close()

# cleaup GPIO pins for next usage
GPIO.cleanup()
    