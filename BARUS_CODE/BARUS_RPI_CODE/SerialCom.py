import serial
import struct
import time
import serial

ser = serial.Serial('/dev/ttyACM2', 57600)


def sendIntToArduino(msg):
    ser.write(struct.pack('>h', msg))


# test ######
def sendStructToArduino(nb1, nb2):
    ser.write(struct.pack('>hh', nb1, nb2))


def readStructFromToArduino():
    msg = ser.read(4)
    val = struct.unpack('<hh', msg)
    print(val[0])
    print(val[1])


#########

def sendStrToArduino(msg):
    ser.write(msg.encode('utf-8'))


def receiveIntFromArduino():
    msg1 = ser.read(2)
    val = struct.unpack('<h', msg1)
    return val[0]


def chekBegin(beginSignal):
    echo = -1
    isOk = False
    sendIntToArduino(beginSignal)
    print("Signal to begin sended")

    while echo != beginSignal:
        echo = receiveIntFromArduino()

        if echo == beginSignal:
            print("Signal to begin received")
            isOk = True
    return isOk

###main test
# test = 4
# sendStructToArduino(test)
# time.sleep(5)


