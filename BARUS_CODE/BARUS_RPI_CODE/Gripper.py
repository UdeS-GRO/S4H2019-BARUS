import SerialCom

gripperSignal = 0
openSignal = 1
closeSignal = 0


def closeGripper():
    msg = 10000 * gripperSignal + closeSignal
    SerialCom.sendIntToArduino(msg)


def openGripper():
    msg = 10000 * gripperSignal + openSignal
    SerialCom.sendIntToArduino(msg)

