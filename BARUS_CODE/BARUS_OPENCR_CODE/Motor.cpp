#include "Motor.h"
#include "Arduino.h"
#include <DynamixelWorkbench.h>
#include <Servo.h>



Motor::Motor(uint32_t Baudrate, const char* DeviceName, uint8_t ID , uint16_t modelNumber){

  model_number = modelNumber;
  motorID = ID;
  baudrate = Baudrate;
  deviceName = DeviceName;
 
  motor.init(deviceName, baudrate);
  
  motor.ping(motorID, &model_number);

}

bool Motor::initWheelMode(){
  return motor.wheelMode(motorID);
}

bool Motor::initMultiTurnMode(){
  
  bool isOk = false;
  if(getOperatingMode() != 4){

    motor.torqueOff(motorID);
    isOk = motor.setExtendedPositionControlMode(motorID);
    motor.torqueOn(motorID);
  }
    return isOk;
}

bool Motor::homing()
{
  initMultiTurnMode();
  return goToPosition(homePosition);
}

int32_t Motor::getOperatingMode(){
  int32_t mode;
  motor.readRegister(motorID,"Operating Mode", &mode);
  
  return mode;
}


bool Motor::goToPosition(int32_t goalPosition){
  initMultiTurnMode();
  int32_t currentPos = getCurrentPosition();
  bool isOk = false;
  isOk = motor.goalPosition(motorID,goalPosition);
  while(getCurrentPosition() < (goalPosition - PRECISION_TOL) || getCurrentPosition() > (goalPosition + PRECISION_TOL)){} // wait while it asn't reach the position +/- precision

  return isOk;
}


bool Motor::rotate(float rotSpeed){
  bool isOk = false;
  float velocity = MAX_SPEED;
  
  motor.torqueOff(motorID);                                                     //pervious mouvement are stopped
  do
  {
    motor.getVelocity(motorID, &velocity);                                      //Make sure the motor has stopped  
  }
  while(velocity > 0.1 || velocity < -0.1);

  initWheelMode();
  if(rotSpeed >= -MAX_SPEED && rotSpeed <= MAX_SPEED)
  {
    if(rotSpeed != 0.0){
      motor.goalVelocity(motorID, rotSpeed);
      isOk = true;
      if(rotSpeed < 0){
        isRollingLeft = false;
        isRollingRight = true;  
      }
      else if(rotSpeed > 0){
        isRollingLeft = true;
        isRollingRight = false;  
      }
    }
    else{
      isRollingLeft = false;
      isRollingRight = false;  
    }
  }
  return isOk;
}

int32_t Motor::getCurrentPosition(){
  int32_t pos = -1;
  motor.getPresentPositionData(motorID, &pos);
  return pos;
}

bool Motor::setHomePos(int pos){
  bool isOk = false;
  if(int32_t(pos) >= MIN_POSITION && int32_t(pos) <= MAX_POSITION )
  {
    homePosition = int32_t(pos);
    isOk = true; 
  }
  return isOk;  
}

int32_t Motor::getHomePos(){ return homePosition; }
