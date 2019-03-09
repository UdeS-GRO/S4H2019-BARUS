import xbox
import time
import SerialCom
import Motor
import Gripper
import Constant
import PositionFileManager


#Main start here

CommunicationIsOk = False


dict = PositionFileManager.initPositionDictionary(Constant.POS_FILE_PATH)

#Establish communication with OPENCR
print("Establish communication with OPENCR...")
if not CommunicationIsOk:
    SerialCom.chekBegin(Constant.BEGIN_SIGNAL)
print("Communication...Ready")

position = Motor.readMotorPosition()

print(position[0])
print(position[1])

PositionFileManager.saveNewPosition("INIT", position[0], position[1], dict , path)

Motor.turnToPos(Constant.MOTOR_1_JOINT, 3000)
Motor.turnToPos(Constant.MOTOR_2_JOINT, 3000)

time.sleep(1)
position = Motor.readMotorPosition()

print(position[0])
print(position[1])

PositionFileManager.saveNewPosition("HOME", position[0], position[1], dict , Constant.POS_FILE_PATH)


