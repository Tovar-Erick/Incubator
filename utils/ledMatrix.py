import serial
import time


arduino=serial.Serial('/dev/ttyACM0',baudrate=9600, timeout = 1.0)
arduino.isOpen()



def flashOn():
    command = 'flash'
    arduino.write('7')
    arduino.close()

def flashOff():
    command = 'flash'
    arduino.write('2')
    arduino.close()
