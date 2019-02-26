# BARUS
Barman Robotisé Révolutionnaire de l'Université de Sherbrooke
(Revolutionary Bartender robot of Sherbrooke's University)

To join this projet on waffle.io: https://waffle.io/thec2511/BARUS/join

Welcome to Barus!

This is an open source project realized by students at the bachelor's degree in robotics engineering from the University of Sherbrooke, Quebec.

The project involves designing a bartender robot to prepare drinks at parties!

Our project is fully open source. You will find attached our codes and the 3D modeling of the robot in SolidWorks.

Material used for this project:

* An OpenCR board;
* A RaspberryPi 3;
* 2 Dynamixel motors XL430-W250-T
* 1 Dynamixel motor XM430-W350-T

Software:

* SolidWorks 2018
* Arduino.ide
* Matlab (to model the robot mathematically)
* QT

Library used for the OpenCR board (to use Dynamixel Motors):

* DynamixelWorkbench: http://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_workbench/#opencr-and-opencm-tutorials   

More information on the OpenCR board: http://emanual.robotis.com/docs/en/parts/controller/opencr10/#examples  

Content of the project:

* Barus_Open_Code: 

   This code is for the OpenCR board.
   
   function.h: Contains our class for serial communication; 
   
   motor.h: contains a class to control the Dynamixel motors; 
   
   ".cpp" file: contains the function definitions;
   
   ".ino" file: contains the main code of the OpenCR board.

* Barus_Rpi_Code:

   This code is for the RaspberryPi. It is used to send commands to the OpenCR board.
   
* CAD:

   This file contains all robot parts developed in SolidWorks.

