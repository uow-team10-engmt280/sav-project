''' 
This program will recieve data from the GPIO pins that are connected to the
Reflectance sensor, each pin is related to it's own sensor. When you get the
data, arrange it into an array or list, then you can use case statements that
then correspond to particular motor speeds
'''

from time import time
import numpy as np
from MachineVisionMain import MV
from typing import Protocol


# TODO should organise each file that needs running so that the entire file is a function that we can import 

# States: IDLE, LISTENING, MOVING, PICKUP, DROPOFF, PARKING, COMPLETED
# Order of state changes: 

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
- Within the MOVING state we may want extra states for different moving phases, or just a counter 
that changes the match case within the MOVING state
- May want to create some functions that make the servos do specific tasks (will be reused in PICKUP and DROPOFF)
- Might want to add a timer so that we know how long it took too complete the race

'''
class State(Protocol):
    def switch(self, sav) -> None:
        ...

# Initialise some values + settings (motor driver mode etc.)
global movPhase
global forkFlag
global pickDropFlag
global mergeFlag
global motorDriverMode

movPhase: str = 'phaseFork'
forkFlag: bool = False
pickDropFlag: bool = False
mergeFlag: bool = False
motorDriverMode: bool = False

class IDLE:
    # Potentially start another programme that will be getting data from the reflectance sensor
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
    
    TParray: list[int] = MV() # FIXME might want to give a different name

    turnOne: int = TParray(0)
    pickUpSideOne: int = TParray(1)
    turnTwo: int = TParray(2)
    pickUpSideTwo: int = TParray(3)
    while(True):
        match input('Decisions received, type "Next" to start race: \n').lower():
            case 'n' | 'Next':
                break
            case _:
                print('Invalid, try again. \n')
    global startTime
    startTime: float = time()
    def switch(self, sav) -> None:
        sav.state = MOVING()


class MOVING:
    print('Entered new state successfully. \n')
    def driving(): # NOTE

        while(True): 
            match movPhase: # Could this be done through attributes?
                case 'phaseFork':
                    if forkFlag == False: # If false then we are at the first fork
                        ...
                    else:
                        ...
                case 'phasePickDrop':
                    if pickDropFlag == False:
                        ...
                    else:
                        ...
                    break
                case 'phaseMerge':
                    if mergeFlag == False:
                        pickDropFlag = True
                    else:
                        ...
                case 'phasePark':
                    ...
                    break
        
    
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
    # Send data to large servo (some method, will need to go up and down)
    # Send data to small servo (some method)
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
    # Might want to do some fancy things like play music or sound to speakers 
    # End programme nicely (stop processes and other programmes, have a nice complete message at the end)

class SAV:
    def __init__(self):
        self.state = IDLE()

    def switch(self) -> None:
        self.state.switch(self)


def main() -> None:
    ...
