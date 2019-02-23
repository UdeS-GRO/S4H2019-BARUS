#ifndef Motor_h
#define Motor_h

#include "Arduino.h"
#include <DynamixelWorkbench.h>
#include <Servo.h>


class Motor
{

  public:
    
   
    Motor(uint32_t Baudrate, const char* DeviceName, uint8_t motorID , uint16_t modelNumber, int32_t velocity, int32_t acceleration);

    bool initJointMode(int32_t velocity, int32_t acceleration);
    void motorTurnLeft(int32_t goalPosition);
    void motorTurnRight(int32_t goalPosition);
    int32_t getCurrentPosition(uint8_t motorID);
    float getCurrentRadianPos(uint8_t motorID);
    //int read_Int();
    //void writeIntToRpi(int msg);

    DynamixelWorkbench motor;

    uint8_t motor_ID;
    uint16_t model_number;
    uint32_t baudrate;
    const char* deviceName;
   
    
    
};


#endif
