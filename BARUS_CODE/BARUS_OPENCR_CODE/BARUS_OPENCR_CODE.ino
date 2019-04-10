



///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//File Name		      : BARUS_OPENCR_CODE
//Date of creation	: 2019/01/30
//Creator		        : BARUS team members - Olivier Girouard, Alexandre Demers
//
//Description		    : The program intiate 3 motors in Joint Mode and receive data from a RasperryPi to control them. A servo is also controlled by the Pi.
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#include <DynamixelWorkbench.h>
#include "Motor.h"
#include "Function.h"
#include <Servo.h>
#include <OpenCR.h>
#include <EEPROM.h>

//---- Define ----//

#define DEVICE_NAME ""
#define BAUDRATE  57600

#define MOTOR_ID_1    1
#define MOTOR_ID_2    2
#define SERVOPIN      3

#define MIN_POSITION 5
#define MAX_POSTITON 4085

#define HOME_POSITION_MOTOR1 5
#define HOME_POSITION_MOTOR2 5

#define TRESHOLD_1 10
#define TRESHOLD_2 20

//---- Detail Declaration ----//

const uint32_t baudrate = BAUDRATE;
const char* deviceName = DEVICE_NAME;

//---- Actuator Declaration ----//
  
Servo gripperServo;
int servoPin = SERVOPIN;

Motor* motor2;
Motor* motor1;

uint8_t motorId_1 = MOTOR_ID_1;
uint8_t motorId_2 = MOTOR_ID_2;

uint16_t motorModel_1 = 0;
uint16_t motorModel_2 = 0;
uint16_t motorModel_3 = 0;


//---- Other Declaration ----//

bool communicationIsOk = false;

int32_t homePositionMotor1 = HOME_POSITION_MOTOR1;
int32_t homePositionMotor2 = HOME_POSITION_MOTOR2;

int precisionTolerence = 10;

void setup() 
{
  Serial.begin(57600);
 
//---- Gripper setup ----//

  gripperServo.attach(servoPin);

//---- Motor setup ----//

  motor1 = new Motor(baudrate, deviceName, motorId_1 , motorModel_1);
  motor2 = new Motor(baudrate, deviceName, motorId_2 , motorModel_2);

  
  motor1->initMultiTurnMode();
  motor2->initMultiTurnMode();

//---- Homming ----//

  
  motor1->setHomePos(1000);
  motor2->setHomePos(2000);

  motor1->homing();
  motor2->homing();
  
  delay(1000);

  openGripper(&gripperServo);
}

void loop()
{

//---- Check communication RPI-OPENCR  ----//
 // checkBegin(&communicationIsOk);
  int actualPos1 = 0;
  int posDiff1 = 0;
  int actualPos2 = 0;
  int posDiff2 = 0;
  
  struct Input inputCommand;
  if(readCommandFromRPI(&inputCommand)){
    switch(inputCommand.function)
    {
      case GRIPPER:
        if(inputCommand.parameter == 1){
          openGripper(&gripperServo);
        }
        else if(inputCommand.parameter == 2){
          closeGripper(&gripperServo);
        }
        break;
        
      case MOTOR_1_WHEEL:
        if(!(motor1->isRollingLeft) && inputCommand.parameter == 1){
          motor1->rotate(2.0);
        }
        else if(!(motor1->isRollingRight) && inputCommand.parameter == 2){
          motor1->rotate(-2.0);
        }
        else{
          motor1->rotate(0.0);
        }
        break;
      
      case MOTOR_2_WHEEL:
        if(!(motor2->isRollingLeft) && inputCommand.parameter == 1){
          motor2->rotate(2.0);
        }
        else if(!(motor2->isRollingRight) && inputCommand.parameter == 2){
          motor2->rotate(-2.0);
        }
        else{
          motor2->rotate(0.0);
        }
        break;
      
      case MOTOR_1_JOINT:
        //motor1->goToPosition(int32_t(inputCommand.parameter));
          actualPos1 = motor1->getCurrentPosition();
          posDiff1 = inputCommand.parameter - actualPos1;
          if (posDiff1 > 0){
            motor1->rotate(2.0);
          }
          else{
            motor1->rotate(-2.0);
          }
          while((actualPos1 < inputCommand.parameter - TRESHOLD_1)||(actualPos1 > inputCommand.parameter + TRESHOLD_1)){
            actualPos1 = motor1->getCurrentPosition();
          }
          motor1->rotate(0.0);
        break;
      
      case MOTOR_2_JOINT:
        //motor2->goToPosition(int32_t(inputCommand.parameter));
          actualPos2 = motor2->getCurrentPosition();
          posDiff2 = inputCommand.parameter - actualPos2;
          if (posDiff2 > 0){
            motor2->rotate(2.0);
          }
          else{
            motor2->rotate(-2.0);
          }
          while((actualPos2 < inputCommand.parameter - TRESHOLD_2)||(actualPos2 > inputCommand.parameter + TRESHOLD_2)){
            actualPos2 = motor2->getCurrentPosition();
          }
          motor2->rotate(0.0);
      
        break;
      
      case MOTOR_1_READ_POS:
        writeIntToRpi(motor1->getCurrentPosition());
        break;
      
      case MOTOR_2_READ_POS:
        writeIntToRpi(motor2->getCurrentPosition());
        break;
        
      case HOME:
        motor1->homing();
        motor2->homing();
        break;
  
    }
  }
}
