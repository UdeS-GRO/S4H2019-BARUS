import SerialCom
import Constant


def turnToPos(commandNb, position):
    #if position >= Constant.POS_MIN:
        SerialCom.send2IntToArduino(commandNb, position)
    #else:
        #print("Goal position excedes limits")


def rotateClockWise(commandNb):
    SerialCom.send2IntToArduino(commandNb, Constant.CLOCKWISE)


def rotateCounterClockWise(commandNb):
    SerialCom.send2IntToArduino(commandNb, Constant.COUNTERCLOCKWISE)


def rotateStop(commandNb):
    SerialCom.send2IntToArduino(commandNb, Constant.STOP)


def readMotorPosition():
    m1Pos = -1
    m2Pos = -1
    SerialCom.send2IntToArduino(Constant.MOTOR_1_READ_POS, 0)
    m1Pos = SerialCom.readIntFromArduino()

    SerialCom.send2IntToArduino(Constant.MOTOR_2_READ_POS, 0)
    m2Pos = SerialCom.readIntFromArduino()

    return (m1Pos, m2Pos)








