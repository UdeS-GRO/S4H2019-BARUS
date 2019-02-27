import SerialCom


#def moveMotor(motorId, position):
    #msg = 10000 * motorId + position
    #SerialCom.sendIntToArduino(msg)
    
def moveMotor(motorId, position):
    SerialCom.sendStructToArduino(motorId, position)

def readMotorPosition(motorId):
    SerialCom.sendIntToArduino(motorId)
    position = SerialCom.receiveIntFromArduino()
    while position < 0 or position > 4092:
        position = SerialCom.receiveIntFromArduino()
    return position
