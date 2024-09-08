''' # TODO should put this into a seperate README file or something along those lines, useful for report. 
This programme is the center of the operation and ties the other programmes together.

It is built off of a Finite State Machine framework, using classes as the states. 

It will first import the Machine Vision programme's main function in to determine both 
the turns the SAV needs to take, as well as the side of pickup and dropoff. 

In the MOVING state we will be importing a list of booleans from the reflectance 
sensor programme that represent the part of the track we are currently driving on, from 
this list we then determine the corresponding/required motor speeds to keep the SAV on 
the track. 

This programme also implements the logic required to pickup and dropoff the 
lego man as well as park, it will be accessing data from the range sensor.

NOTE Could put the range sensor logic into a seperate programme, may need to see how 
much this affects perform, but the code would be pretty simple (maybe motor driver too?)
'''

# TODO should organise each file that needs running so that the entire file is a function that we can import 

# IDLE --> LISTENING
# LISTENING --> MOVING
# MOVING --> PICKUP
# PICKUP --> MOVING
# MOVING --> DROPOFF
# DROPOFF --> MOVING
# MOVING --> PARKING
# PARKING --> COMPLETED

'''
NOTE 
- May want to create some functions that make the servos do specific tasks (will be reused in PICKUP and DROPOFF)

'''
import RPi.GPIO as GPIO # type: ignore 
from time import time
from typing import Protocol
from MachineVisionMain import MV 
from FindCase import FindCase

class State(Protocol):
    def switch(self, sav) -> None:
        ...

class SAV:
    def __init__(self):
        self.state = IDLE()
        global phaseA
        global enableA
        global phaseB
        global enableB

        phaseA = 6
        enableA = 13
        phaseB = 19
        enableB = 26
        smallServoCtrl = 5
        largeServoCtrl = 0
        rangeSense = 2


        GPIO.setmode(GPIO.BCM)
        GPIO.setup(phaseA, GPIO.OUT)
        GPIO.setup(enableA, GPIO.OUT) # THIS PIN SUPPORTS PWM
        GPIO.setup(phaseB, GPIO.OUT)
        GPIO.setup(enableB, GPIO.OUT) # THIS PIN DOES NOT SUPPORT PWM, GPIO12 DOES SUPPORT PWM
        GPIO.setup(largeServoCtrl, GPIO.OUT) # SMALL SERVO
        GPIO.setup(smallServoCtrl, GPIO.OUT) # LARGE SERVO
        GPIO.setup(rangeSense, GPIO.IN) # RANGE SENSOR
        
        GPIO.output(phaseA, GPIO.LOW)
        GPIO.output(enableA, GPIO.LOW)
        GPIO.output(phaseB, GPIO.LOW)
        GPIO.output(enableB, GPIO.LOW)



        global movPhase
        global forkFlag
        global pickDropFlag
        global mergeFlag
        global motorDriverMode
        global turnOne
        global turnTwo
        global pickUpSideOne
        global pickUpSideTwo
        global motorInstruc

        movPhase: str = 'phaseFork'
        forkFlag: bool = False
        pickDropFlag: bool = False
        mergeFlag: bool = False
        motorDriverMode: bool = False



    def switch(self) -> None:
        self.state.switch(self)

class IDLE:
    while(True):
        match input('Type "Start" to begin program when you\'re ready: \n').lower():
            case 's' | 'start':
                break
            case _:
                print('Invalid, try again. \n')
    def switch(self, sav) -> None:
        sav.state = LISTENING()
        print('Changing state')

class LISTENING:
    print('Entered new state successfully. \n')
    
    # May want to wait until the Machine Vision programme is fully done

    TParray: list[bool] = MV() 
    turnOne: bool = TParray(0)
    pickUpSideOne: bool = TParray(1)
    turnTwo: bool = TParray(2)
    pickUpSideTwo: bool = TParray(3)
    

    # Start reflectance sensor programme
    while(True):
        match input('Decisions received, type "Next" to start race: \n').lower():
            case 'n' | 'next':
                break
            case _:
                print('Invalid, try again. \n')

    global startTime
    startTime: float = time()
    def switch(self, sav) -> None:
        sav.state = MOVING()


class MOVING:
    print('Entered new state successfully. \n')
    def driving():
        while(True): 
            if movPhase == 'phasePickDrop' | 'phasePark':
                if rangeSense == 1:
                    ... # Stop driving/moving
                else:
                    motorInstruc = FindCase()
                    # phaseA = motorInstruc(0)
                    # enableA = motorInstruc(1)
                    # phaseB = motorInstruc(2)
                    # enableB = motorInstruc(3)

            else:
                motorInstruc = FindCase()
                # phaseA = motorInstruc(0)
                # enableA = motorInstruc(1)
                # phaseB = motorInstruc(2)
                # enableB = motorInstruc(3)


    # Sends the decision to the motor driver to turn the sav accordingly
    
    if pickDropFlag == False:
        def switch(self, sav) -> None:
            sav.state = PICKUP()
    else:
        def switch(self, sav) -> None:
            sav.state = DROPOFF()

class PICKUP:
    print('Entered new state successfully. \n')
    # NOTE Should at some point indicate that this state has been jumped to so that sav moves to the next MOVING phase
    # Should stop the sav (send data to the motor driver)
    # Potentially change motor driver mode
    # Potentially fix position (to ensure it picks up in right place)
    # Send data to large servo (some function, will need to go up and down)
    # Send data to small servo (some function)
    # Once PICKUP is complete, should change state like done here:
    def switch(self, sav) -> None:
        sav.state = MOVING()

class DROPOFF:
    print('Entered new state successfully. \n')
    # Essentially it needs to complete the same task in PICKUP but maybe a different order or values
    # Once DROPOFF is complete, move to next state like done here:
    def switch(self, sav) -> None:
        sav.state = MOVING()

class PARKING:
    print('Entered new state successfully. \n')
    # Should stop, re-adjust if needed 
    # NOTE not sure if any other tasks need to be complete during this state
    def switch(self, sav) -> None:
        sav.state = COMPLETE()

class COMPLETE:
    print('Entered new state successfully.')
    endTime: float = time()
    raceTime: float = endTime - startTime
    minutes: int = raceTime//60
    seconds: float = raceTime%60
    print('You took %d minutes and %f seconds to complete the track. ' % (minutes, seconds))

    # End programme nicely (stop processes and other programmes, have a nice complete message at the end)



def main() -> None:
    ...
