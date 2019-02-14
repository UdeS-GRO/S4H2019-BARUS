///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//Program Name		  : InitiateMotor.py
//Date of creation	: 2019/01/30
//Creator		        : BARUS team members - Olivier Girouard, Alexandre Demers
//
//Description		    : The program intiate 3 motors in Joint Mode and make them mode at the and to make sure the communication is OK
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#include <DynamixelWorkbench.h>
#include "Motor.h"
#include <Servo.h>


#define DEVICE_NAME ""
#define BAUDRATE  57600

#define MOTOR_ID_1    1
#define MOTOR_ID_2    2
#define MOTOR_ID_3    3
#define SERVOPIN      3

/* Creation of motor and servo objects */
Servo gripperServo;



void setup() 
{
  Serial.begin(57600);

  const uint32_t baudrate = BAUDRATE;
  const char* deviceName = DEVICE_NAME;


  uint8_t motorId_1 = MOTOR_ID_1;
  uint8_t motorId_2 = MOTOR_ID_2;
  uint8_t motorId_3 = MOTOR_ID_3;
  
  uint16_t motorModel_1 = 0;
  uint16_t motorModel_2 = 0;
  uint16_t motorModel_3 = 0;

  int servoPin = SERVOPIN;

  // Creat motor objects set for joint mode
  Motor motor1(baudrate, deviceName, motorId_1 , motorModel_1, 0, 0);
  Motor motor2(baudrate, deviceName, motorId_2 , motorModel_2, 0, 0);
  Motor motor3(baudrate, deviceName, motorId_3 , motorModel_3, 0, 0);

  //test on motors
  /*
  motor1.motorTurnLeft(0);
  delay(3000);
  motor1.motorTurnLeft(1023);
  delay(3000);
  */
  motor1.motorTurnLeft(0);
  delay(3000);
  motor1.motorTurnLeft(800);
  delay(3000);
  motor1.motorTurnLeft(1200);
  delay(3000);
  motor1.motorTurnLeft(2000);
  delay(3000);
  

  //control servo gripper
  gripperServo.attach(servoPin);
  gripperServo.write(0);
  delay(2000);
  gripperServo.write(90);
  delay(2000);
  gripperServo.write(0);
  delay(1000);
    
    
    
  

 }


void loop() 
{

}
