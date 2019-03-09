#ifndef Motor_h
#define Motor_h

#include "Arduino.h"
#include <DynamixelWorkbench.h>
#include <Servo.h>

#define MIN_POSITION 5
#define MAX_POSITION 4085
#define MAX_SPEED 8.0
#define PRECISION_TOL 3

class Motor
{

  public:
    
    
//---- METHODS ----//   
    Motor(uint32_t Baudrate, const char* DeviceName, uint8_t ID , uint16_t modelNumber);


    bool initWheelMode();
    bool initMultiTurnMode();
    bool homing();
    int32_t getOperatingMode();
    

    bool goToPosition(int32_t goalPosition);
    bool rotate(float rotSpeed);
    
    int32_t getCurrentPosition();

    bool setHomePos(int pos = 5);
    int32_t getHomePos();

//---- ATTRIBUTES ----//  
    DynamixelWorkbench motor;

    int32_t homePosition = 5;
    int32_t maxPos = MAX_POSITION;
    int32_t minPos = MIN_POSITION;
    
    uint8_t motorID;
    uint16_t model_number;
    uint32_t baudrate;
    const char* deviceName;
    bool isRollingLeft = false;
    bool isRollingRight = false;

    
   
    
    
};


#endif
