import os

#Function numbers to connect in openCr
CLOCKWISE = 2
COUNTERCLOCKWISE = 1
STOP = 0
GRIPPER = 1
MOTOR_1_WHEEL = 2
MOTOR_2_WHEEL= 3
MOTOR_1_JOINT= 4
MOTOR_2_JOINT= 5
MOTOR_1_READ_POS= 6
MOTOR_2_READ_POS= 7
HOME= 8
NOTHING= 9
WAIT = 1.5
WAIT_SHOT = 5
DEF_HEIGHT = 2100
POUR_1OZ = 7
POUR_2OZ = 10

GRIPPER_OPEN = 1
GRIPPER_CLOSE = 2

MOTOR1_ID = 1
MOTOR2_ID = 2

POS_MIN = 5


curWorkDir = os.getcwd()                    # current working directory
curWorkDir = curWorkDir.replace("\\", "/")
POS_FILE_PATH = curWorkDir + "/PositionFile.txt"

BEGIN_SIGNAL = 420


