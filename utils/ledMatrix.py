import serial
from time import sleep

def connectSerial():
    try:
        arduino=serial.Serial('/dev/ttyACM0',baudrate=9600, timeout = 1.0)
        if(arduino.isOpen() == False):
            arduino.open()
    except IOError: # if port is already opened, close it and open it again and print message
        print('Trying serial re-connection...')
        arduino.close()
        arduino.open()
        print ("port was already open, was closed and opened again!")

    # Wake Modem
    # arduino.setDTR(True)
    # sleep(3)
    # arduino.setDTR(False)
    sleep(3)

    # Start talking
    arduino.setDTR(True)
    return arduino

def sendSerialCommand(command, value):
    print('Sending {}, {}'.format(command, value))
    # arduino = connectSerial()
    arduino.write('{},{}'.format(command, value))
    sleep(4)
    #print('Me llego: {}'.format(''.join(arduino.readline().splitlines())))
    # arduino.close()

def closeConnection():
    arduino.close()

def lightRB(redLightPercentage): # Value parameter is the Red percentage
    command = 'RB'
    sendSerialCommand(command, redLightPercentage)

def flashOn(intensity): # with intensity 0<=intensity<=255
    command = 'Flash'
    sendSerialCommand(command, intensity)
    sleep(2)

def adjustBrightness(intensity):
    command = 'Brightness'
    sendSerialCommand(command, intensity)

def demo():
    lightRB(0)
    adjustBrightness(50)
    lightRB(100)
    adjustBrightness(100)
    flashOn(150)
    adjustBrightness(100)
    lightRB(50)


arduino = connectSerial()
if __name__ == '__main__':
    demo()
    closeConnection()
