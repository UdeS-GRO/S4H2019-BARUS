import SerialCom

gripperFunctionNB = 1
openSignal = 1
closeSignal = 2


def closeGripper():
    SerialCom.sendStructToArduino(gripperFunctionNB, closeSignal)


def openGripper():
    SerialCom.sendStructToArduino(gripperFunctionNB, openSignal)

