import serial
import struct
import time
import Constant

ser = serial.Serial('COM3', 57600)

def sendIntToArduino(msg):
    ser.write(struct.pack('>h', msg))


def readIntFromArduino():
    msg1 = ser.read(2)
    val = struct.unpack('<h', msg1)
    return val[0]


def send2IntToArduino(nb1, nb2):
    ser.write(struct.pack('>hh', nb1, nb2))


def read2IntFromToArduino():
    msg = ser.read(4)
    val = struct.unpack('<hh', msg)
    print(val[0])
    print(val[1])


def chekBegin(beginSignal):
    echo = -1
    isOk = False
    for i in range(0,10):
        sendIntToArduino(beginSignal)

    while echo != beginSignal:
        echo = readIntFromArduino()

        if echo == beginSignal:
            isOk = True

    return isOk



