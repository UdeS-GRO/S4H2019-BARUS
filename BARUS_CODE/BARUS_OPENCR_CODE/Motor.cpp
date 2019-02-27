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


bool Motor::initJointMode(){
  return motor.jointMode(motorID);
}

bool Motor::initWheelMode(){
  return motor.wheelMode(motorID);
}

void Motor::homing()
{
  initJointMode();
  motor.goalPosition(motorID, homePosition);
  delay(500);
}

void Motor::motorTurnLeft(int32_t goalPosition )
{
  bool result = false;
  result = motor.setReverseDirection(motorID);
  motor.goalPosition(motorID, goalPosition);
}


void Motor::motorTurnRight(int32_t goalPosition)
{
  bool result = false;
  result = motor.setNormalDirection(motorID);
  motor.goalPosition(motorID, goalPosition);
}


bool Motor::rotate(float rotSpeed){
  bool isOk = false;
  float velocity = MAX_SPEED;
  
  motor.torqueOff(motorID);
  do
  {
    motor.getVelocity(motorID, &velocity);
  }
  while(velocity > 0.1 || velocity < -0.1);
  
  motor.torqueOn(motorID);
  if(rotSpeed >= -MAX_SPEED && rotSpeed <= MAX_SPEED)
  {
    motor.goalVelocity(motorID, rotSpeed);
    isOk = true;
  }
  return isOk;
}

int32_t Motor::getCurrentPosition(uint8_t motorID)
{

  bool isRead = false;
  int32_t pos;
  isRead = motor.getPresentPositionData(motorID, &pos);
  if(!isRead)
  {
    return -1;
  }
  return pos; 
}

float Motor::getCurrentRadianPos(uint8_t motorID)
{
  bool isRead = false;
  float pos;
  isRead = motor.getRadian(motorID, &pos);
  if(!isRead)
  {
    return -1;
  }
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
