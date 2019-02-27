import xbox
# import serial
# import struct
import time
import SerialCom
import Motor
import Gripper

# Main start here

motor1_ID = 1
motor2_ID = 2
# motor3_ID = 3

rotationMax = 4085
rotationMin = 5

beginSignal = 420

CommunicationIsOk = False

# enum Function{
GRIPPER = 1
MOTOR_1_WHEEL = 2
MOTOR_2_WHEEL = 3
MOTOR_1_JOINT = 4
MOTOR_2_JOINT = 5
MOTOR_1_READ_POS = 6
MOTOR_2_READ_POS = 7
HOME = 8
NOTHING = 9
#  };

# Establish communication with OPENCR
print("Establish communication with OPENCR...")
if not CommunicationIsOk:
    SerialCom.chekBegin(beginSignal)
print("Communication...Ready")

ctrl = xbox.Joystick()

# --------------- First recepe Rhum-N-Coke ---------------#
print("Recepe: Rhum-N-Coke")
# Going to cup station for pickup

print("Going to cup station for pickup")
while not ctrl.Start():
    if ctrl.A() and not ctrl.Y():
        SerialCom.sendStructToArduino(2, 1)
    elif not ctrl.A() and ctrl.Y():
        SerialCom.sendStructToArduino(2, 2)
    elif ctrl.rightBumper():
        SerialCom.sendStructToArduino(2, 0)

    if ctrl.X() and not ctrl.B():
        SerialCom.sendStructToArduino(3, 1)
    elif not ctrl.X() and ctrl.B():
        SerialCom.sendStructToArduino(3, 2)
    elif ctrl.leftBumper():
        SerialCom.sendStructToArduino(3, 0)

    time.sleep(0.1)
    # SerialCom.sendStructToArduino(3,1)
    # print(SerialCom.receiveIntFromArduino())
    # time.sleep(1)
    # print(SerialCom.receiveIntFromArduino())

ctrl.close()

#SerialCom.sendStructToArduino(3, 1)
#time.sleep(3)
#SerialCom.sendStructToArduino(3, 2)
#time.sleep(3)
#SerialCom.sendStructToArduino(3, 0)
#time.sleep(3)

#SerialCom.sendStructToArduino(2, 1)
#time.sleep(3)
#SerialCom.sendStructToArduino(2, 2)
#time.sleep(3)
#SerialCom.sendStructToArduino(2, 0)
#time.sleep(3)

#SerialCom.sendStructToArduino(4, 1000)
#time.sleep(1)
#SerialCom.sendStructToArduino(4, 2000)
#time.sleep(1)
#SerialCom.sendStructToArduino(4, 3000)
#time.sleep(1)
#SerialCom.sendStructToArduino(4, 10)
#time.sleep(1)

#SerialCom.sendStructToArduino(5, 1000)
#time.sleep(1)
#SerialCom.sendStructToArduino(5, 2000)
#time.sleep(1)
#SerialCom.sendStructToArduino(5, 3000)
#time.sleep(1)
#SerialCom.sendStructToArduino(5, 10)
#time.sleep(1)