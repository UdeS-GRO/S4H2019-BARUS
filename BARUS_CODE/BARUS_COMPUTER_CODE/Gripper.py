import SerialCom
import Constant


def closeGripper():
    SerialCom.send2IntToArduino(Constant.GRIPPER, Constant.GRIPPER_CLOSE)


def openGripper():
    SerialCom.send2IntToArduino(Constant.GRIPPER, Constant.GRIPPER_OPEN)



