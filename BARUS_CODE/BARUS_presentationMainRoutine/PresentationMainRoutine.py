import xbox
#import serial
#import struct
import time
import SerialCom
import Motor
import Gripper

#Main start here

motor1_ID = 1
motor2_ID = 2
motor3_ID = 3

rotationMax = 2700
rotationMin = 5

beginSignal = 420

CommunicationIsOk = False

#Establish communication with OPENCR
print("Establish communication with OPENCR...")
if not CommunicationIsOk:
    SerialCom.chekBegin(beginSignal)
print("Communication...Ready")


#--------------- First recepe Rhum-N-Coke ---------------#
print("Recepe: Rhum-N-Coke")
# Going to cup station for pickup

print("Going to cup station for pickup")
Motor.moveMotor(motor1_ID, 1023)
time.sleep(0.5)
Motor.moveMotor(motor2_ID, 2046)
time.sleep(0.5)
Motor.moveMotor(motor3_ID, rotationMax)
time.sleep(2)

# Close gripper to take cup

print("Close gripper to take cup")
Gripper.closeGripper()
time.sleep(2)

# Go to first buttle Coke

print("Go to first buttle - Coke")
Motor.moveMotor(motor1_ID, rotationMin)
time.sleep(0.5)
Motor.moveMotor(motor2_ID, rotationMin)
time.sleep(0.5)
Motor.moveMotor(motor3_ID, rotationMin)
time.sleep(2)

# Pour product 1 - Coke

print("Pour product 1 - Coke")
Motor.moveMotor(motor3_ID, 2046)
time.sleep(4)
Motor.moveMotor(motor3_ID, rotationMin)
time.sleep(2)

# Go to next buttle - Rhum

print("Go to next buttle - Rhum")
Motor.moveMotor(motor1_ID, rotationMax)
time.sleep(0.5)
Motor.moveMotor(motor2_ID, rotationMax)
time.sleep(0.5)
Motor.moveMotor(motor3_ID, rotationMax)
time.sleep(2)

# Pour product 1 - Rhum

print("Pour product 1 - Rhum")
Motor.moveMotor(motor3_ID, 2046)
time.sleep(2)
Motor.moveMotor(motor3_ID, rotationMax)
time.sleep(2)

# Go to cup station for release

print("Go to cup station for release")
Motor.moveMotor(motor1_ID, rotationMin)
time.sleep(0.5)
Motor.moveMotor(motor2_ID, rotationMin)
time.sleep(0.5)
Motor.moveMotor(motor3_ID, rotationMin)
time.sleep(2)

# Open gripper to release cup

print("Open gripper to release cup")
Gripper.openGripper()
time.sleep(2)

# Go to home position

print("Go to home position")
Motor.moveMotor(motor1_ID, rotationMax)
time.sleep(0.5)
Motor.moveMotor(motor2_ID, rotationMax)
time.sleep(0.5)
Motor.moveMotor(motor3_ID, rotationMax)
time.sleep(2)

