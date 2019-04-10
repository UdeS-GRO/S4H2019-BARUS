#ifndef Function_h
#define Function_h

#include "Arduino.h"
#include <DynamixelWorkbench.h>
#include <Servo.h>

#define READY_SIGNAL 420 
#define COMMUNICATION_SIGNAL 420 
#define GRIPPER_OPEN_ANGLE 85
#define GRIPPER_CLOSE_ANGLE 5

enum Function{
  GRIPPER = 1,
  MOTOR_1_WHEEL,
  MOTOR_2_WHEEL,
  MOTOR_1_JOINT,
  MOTOR_2_JOINT,
  MOTOR_1_READ_POS,
  MOTOR_2_READ_POS,
  HOME,
  NOTHING
  };

typedef struct Input{
  
  int function = 0;
  int parameter = 0;
  
};

void openGripper(Servo* gripperServo){
  gripperServo->write(GRIPPER_OPEN_ANGLE);  
}
void closeGripper(Servo* gripperServo){
  gripperServo->write(GRIPPER_CLOSE_ANGLE);  
}

void writeIntToRpi(int msg) 
{ 
  Serial.write(lowByte(msg));
  Serial.write(highByte(msg));
}

void emptySerialPort()
{
  while(Serial.available() > 0)
  {
    Serial.read();  
  }
}

void signalReadyToRead()
{
  writeIntToRpi(READY_SIGNAL); 
}

bool readCommandFromRPI(struct Input* command) 
{
  int Byte1 = 0;
  int Byte2 = 0;
  int Byte3 = 0;
  int Byte4 = 0;
  bool isOk = false;

  if(Serial.available() > 0)
  {
    Byte1 = Serial.read();
    Byte2 = Serial.read(); 
    Byte3 = Serial.read();
    Byte4 = Serial.read();
    command->function = ((Byte1<<8) + Byte2);
    command->parameter = ((Byte3<<8)+Byte4);
    isOk = true;
    
  }
  //emptySerialPort();
  //signalReadyToRead();
  
  return isOk; 
}

int readIntFromRPI() 
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
}

void checkBegin(bool* ptrIsBegin)
{
  int signalToBegin = 0;
  while(!(*ptrIsBegin))
  {
    signalToBegin = readIntFromRPI();
    if(signalToBegin == COMMUNICATION_SIGNAL)  
    {
      *ptrIsBegin = true;
      writeIntToRpi(COMMUNICATION_SIGNAL);
    }
  }
}











 
#endif
