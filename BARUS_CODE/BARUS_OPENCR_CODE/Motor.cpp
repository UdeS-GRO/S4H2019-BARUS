#include "Motor.h"
#include "Arduino.h"
#include <DynamixelWorkbench.h>
#include <Servo.h>



Motor::Motor(uint32_t Baudrate, const char* DeviceName, uint8_t motorID , uint16_t modelNumber, int32_t velocity, int32_t acceleration){

  bool isOk;
  
  model_number = modelNumber;
  motor_ID = motorID;
  baudrate = Baudrate;
  deviceName = DeviceName;
  isOk = initJointMode(velocity, acceleration);

}


bool Motor::initJointMode(int32_t velocity, int32_t acceleration){
  const char *log;
  bool result = false;
  
  result = motor.init(deviceName, baudrate, &log);
  result = motor.ping(motor_ID, &model_number, &log);
  result = motor.jointMode(motor_ID, velocity, acceleration, &log);

  return result;
}

void Motor::motorTurnLeft(int32_t goalPosition )
{
  const char *log;
  bool result = false;
  result = motor.setNormalDirection(motor_ID, &log);
  motor.goalPosition(motor_ID, goalPosition);
}


void Motor::motorTurnRight(int32_t goalPosition)
{
  const char *log;
  bool result = false;
  result = motor.setReverseDirection(motor_ID, &log);
  motor.goalPosition(motor_ID, goalPosition);
}

int32_t Motor::getCurrentPosition(uint8_t motorID)
{
  const char *log;
  bool isRead = false;
  int32_t pos;
  isRead = motor.getPresentPositionData(motorID, &pos, &log);
  if(!isRead)
  {
    return -1;
  }
  return pos; 
}

float Motor::getCurrentRadianPos(uint8_t motorID)
{
  const char *log;
  bool isRead = false;
  float pos;
  isRead = motor.getRadian(motorID, &pos, &log);
  if(!isRead)
  {
    return -1;
  }
  return pos; 
}

// Function for reading strings from Raspberry Pi
/*int Motor::read_Int() 
{
  int Byte1 = 0;
  int Byte2 = 0;
  if(Serial.available() > 0)
  {
    Byte1 = Serial.read();
    Byte2 = Serial.read(); 
    return ((Byte1<<8) + Byte2);  
  }
  return -1; 
}*/

// Function for sending a string to RaspberryPi
/*void Motor::writeIntToRpi(int msg) 
{ 
 Serial.write(lowByte(msg));
 Serial.write(highByte(msg));
 
}*/
