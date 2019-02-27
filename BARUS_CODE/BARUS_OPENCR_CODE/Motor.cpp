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

bool Motor::homing()
{
  initJointMode();
  return motor.goalPosition(motorID, homePosition);
}

/*void Motor::motorTurnLeft(int32_t goalPosition )
{
  //result = motor.setReverseDirection(motorID);
  motor.goalPosition(motorID, goalPosition);
}


void Motor::motorTurnRight(int32_t goalPosition)
{
  //result = motor.setNormalDirection(motorID);
  motor.goalPosition(motorID, goalPosition);
}*/

bool Motor::turnToPos(int32_t goalPosition)
{ 
  bool isOk = false;
  if (goalPosition <= maxPos && goalPosition >= minPos)
  {
    isOk = true;
    motor.torqueOff(motorID);                                                   //pervious mouvement are stopped
    initJointMode();                                                            //TorqueOn() built in -> enable mouvement instruction
    motor.goalPosition(motorID, goalPosition);
  }
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

int Motor::getCurrentPosition()
{
  int32_t pos = -1;
  motor.getPresentPositionData(motorID, &pos);
  return pos;
}

/*float Motor::getCurrentRadianPos(uint8_t motorID)
{
  bool isRead = false;
  float pos;
  isRead = motor.getRadian(motorID, &pos);
  if(!isRead)
  {
    return -1;
  }
  return pos; 
}*/

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
