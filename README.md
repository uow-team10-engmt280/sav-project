# ENGMT280 SAV project git repo


## INFOMATION:

The sequence of state changes:
IDLE --> LISTENING
LISTENING --> MOVING
MOVING --> PICKUP
PICKUP --> MOVING
MOVING --> DROPOFF
DROPOFF --> MOVING
MOVING --> PARKING
PARKING --> COMPLETED

## Here are the GPIO pins **FOR HAMMAD'S PCB

    For Reflectance Sensor:
        - GPIO23 --> Pin 1 
        - GPIO20 --> Pin 2
        - GPIO24 --> Pin 3
        - GPIO16 --> Pin 4
        - GPIO25 --> Pin 5
        - GPIO12 --> Pin 6
        - GPIO8  --> Pin 7
        - GPIO1  --> Pin 8
        - GPIO7  --> Pin 9

        - GPIO18 --> ODD control
        - GPIO21 --> EVEN control
    Note that pin 1 on the reflectance sensor is the one furthest to the left if actually looking at the sensors (IR LED and phototransistor facing you)

    To be used as OUTPUT:
        - GPIO6 --> PHASEA (motor driver, ON/OFF)
        - GPIO13 --> ENABLEA (motor driver, speed in %)
        - GPIO19 --> PHASEB (motor driver, ON/OFF)
        - GPIO26 --> ENABLEB (motor driver, speed in %)
        - GPIO5 --> Small servo Control
        - GPIO0 --> Large servo Control
    To be used as INPUT:
        - GPIO2 --> Range sensor output  


## FOR MATT'S PCB:

For Reflectance Sensor:
        - GPIO --> Pin 1 
        - GPIO --> Pin 2
        - GPIO --> Pin 3
        - GPIO --> Pin 4
        - GPIO --> Pin 5
        - GPIO --> Pin 6
        - GPIO  --> Pin 7
        - GPIO  --> Pin 8
        - GPIO  --> Pin 9

        - GPIO --> ODD control
        - GPIO --> EVEN control
    Note that pin 1 on the reflectance sensor is the one furthest to the left if actually looking at the sensors (IR LED and phototransistor facing you)

    To be used as OUTPUT:
        - GPIO --> PHASEA (motor driver, ON/OFF)
        - GPIO --> ENABLEA (motor driver, speed in %)
        - GPIO --> PHASEB (motor driver, ON/OFF)
        - GPIO --> ENABLEB (motor driver, speed in %)
        - GPIO --> Small servo Control
        - GPIO --> Large servo Control
    To be used as INPUT:
        - GPIO --> Range sensor output  


### REMINDERS/WHAT NEEDS DOING:
1. Could create seperate functions to control the servos in another file to just import and call them. DONE

2. Don't forget to remove some comments like "# type: ignore", this is used to ignore problems that 
we know aren't problems, but should remove later just incase there are problems.

3. Maybe add something to the SystemLogic programme (or MachineVisionMain??) to wait until the correct list has
been returned through the function

4. What would "end the programme nicely" entail - (not actually sure if this is a thing or if it just involves
GPIO cleanup)

5. NEED TO FIX THE "MachineVisionMain.py" PROGRAMME***
