import serial
import struct
ser = serial.Serial('/dev/ttyUSB0', 9600)

def sendIntToArduino(msg):
    ser.write(struct.pack('>h', msg))

def sendStrToArduino(msg):
    ser.write(msg.encode('utf-8'))

def receiveIntFromArduino():
    msg1 = ser.read(2)
    val = struct.unpack('<h',msg1)
    print(val[0])
    return val

for i in range(0,10):
    sendIntToArduino(5000)
    receiveIntFromArduino()

    
