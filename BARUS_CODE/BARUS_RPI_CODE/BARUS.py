import xbox
import serial
import struct
import time

ser = serial.Serial('/dev/ttyACM0', 57600)


def sendIntToArduino(msg):
    ser.write(struct.pack('>h', msg))


def sendStrToArduino(msg):
    ser.write(msg.encode('utf-8'))


def receiveIntFromArduino():
    msg1 = ser.read(2)
    val = struct.unpack('<h', msg1)
    return val[0]


def chekBegin(beginSignal):
    echo = -1

    sendIntToArduino(beginSignal)
    print("Signal to begin sended")

    while echo != beginSignal:
        echo = receiveIntFromArduino()

        if echo == beginSignal:
            print("Signal to begin received")
            print(echo)


def moveMotor(motorId, position):
    msg = 10000 * motorId + position
    sendIntToArduino(msg)
    print(msg)


def readMotorPosition(motorId):
    sendIntToArduino(50000 + motorId)
    position = receiveIntFromArduino
    while position < 0 or position > 4092:
        position = receiveIntFromArduino
    return position


# Main start here

motor1_Id = 1
motor2_Id = 2
motor3_Id = 3

rotationMax = 4085
rotationMin = 5

beginSignal = 420

joy = xbox.Joystick()

chekBegin(beginSignal)

while not joy.X():
    if joy.A() and not joy.Y():
        sendIntToArduino(30001)
        print("A pressed")
    elif not joy.A() and joy.Y():
        sendIntToArduino(30000)
        print("Y pressed")
    else:
        sendIntToArduino(0)
        print("A/Y released")
    time.sleep(0.1)

print("X pressed")

joy.close()






