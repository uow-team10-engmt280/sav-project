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

#  `  ~  q  Q  c  A   1  !

'''
NOTE 
- May want to create some functions that make the servos do specific tasks (will be reused in PICKUP and DROPOFF)

'''
# import RPi.GPIO as GPIO
import numpy as np # NOTE Currently unused
from time import time
from typing import Protocol
from MachineVisionMain import MV 


class State(Protocol):
    def switch(self, sav) -> None:
        ...

# Initialise some values + settings (motor driver mode etc.) NOTE is there a cleaner way to initialise values?
global movPhase
global forkFlag
global pickDropFlag
global mergeFlag
global motorDriverMode
global turnOne
global turnTwo
global pickUpSideOne
global pickUpSideTwo

movPhase: str = 'phaseFork'
forkFlag: bool = False
pickDropFlag: bool = False
mergeFlag: bool = False
motorDriverMode: bool = False

class IDLE:
    while(True):
        match input('Type "Start" to begin program when you\'re ready: \n').lower():
            case 's' | 'start':
                break
            case _:
                print('Invalid, try again. \n')
                ...
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
            ...
            
        
    
    # It needs to request data from the reflectance sensor (might activate/start reflectance sensor programme or just request the list/array)
    # Selects a decision about motor speeds based upon the list/array received in the previous step
    # Sends the decision to the motor driver to turn the sav accordingly
    # Depending upon the phase, may be listening to the range sensor, if this is the case then if the RS returns a 1, move to next state/break from while loop

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

class SAV:
    def __init__(self):
        self.state = IDLE()

    def switch(self) -> None:
        self.state.switch(self)


def main() -> None:
    ...
