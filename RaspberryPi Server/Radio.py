import RPi.GPIO as GPIO
import time
import subprocess

'''
Sets up GPIO pins for usage
'''
def setUp():
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

'''
Sends switch command to given device

socket: target device
state: state to switch too
'''
def switchSocket(socket, state):
    output = [True, True, True, True]
    output[3] = True if(state) else False

    if(socket == 1):
        output[0] = True 
        output[1] = True
        output[2] = True
    
    if(socket == 2):
        output[0] = False 
        output[1] = True
        output[2] = True

    if(socket == 3):
        output[0] = True 
        output[1] = False
        output[2] = True

    if(socket == 4):
        output[0] = False 
        output[1] = False
        output[2] = True

    
    print(output[0], ": ", output[1], ": ", output[2], ": ", output[3])

    GPIO.output (11, output[0])
    GPIO.output (15, output[1])
    GPIO.output (16, output[2])
    GPIO.output (13, output[3])
    # let it settle, encoder requires this
    time.sleep(0.1)	
    # Enable the modulator
    GPIO.output (22, True)
    # keep enabled for a period
    time.sleep(0.25)
    # Disable the modulator
    GPIO.output (22, False)

'''
Cleans up GPIO pins after usage
'''
def cleanUp():
    GPIO.cleanup()