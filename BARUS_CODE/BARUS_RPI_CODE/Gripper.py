import SerialCom

gripperSignal = 0
openSignal = 1
closeSignal = 0


#def openGripper():
    #msg = 10000 * gripperSignal + openSignal
    #SerialCom.sendIntToArduino(msg)
#def closeGripper():
    #msg = 10000 * gripperSignal + closeSignal
    #SerialCom.sendIntToArduino(msg)
def closeGripper():
    SerialCom.sendStructToArduino(gripperSignal, closeSignal)
def openGripper():
    SerialCom.sendStructToArduino(gripperSignal, openSignal)



