#include "Motor.h"
#include "Arduino.h"
#include <DynamixelWorkbench.h>
#include <Servo.h>



Motor::Motor(uint32_t Baudrate, const char* DeviceName, uint8_t motorID , uint16_t modelNumber, int32_t velocity, int32_t acceleration){

  model_number = modelNumber;
  motor_ID = motorID;
  baudrate = Baudrate;
  deviceName = DeviceName;
  initJointMode(velocity, acceleration);
  Serial.println("Motor object created");
}


void Motor::initJointMode(int32_t velocity, int32_t acceleration){
  const char *log;
  bool result = false;
  
  result = motor.init(deviceName, baudrate, &log);
  result = motor.ping(motor_ID, &model_number, &log);
  if (result == false)
  {
    Serial.println(log);
    Serial.println("Failed to ping");
  }
  else
  {
    Serial.println("Succeeded to ping");
    Serial.print("id : ");
    Serial.print(motor_ID);
    Serial.print(" model_number : ");
    Serial.println(model_number);
  }
  result = motor.jointMode(motor_ID, velocity, acceleration, &log); 
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
