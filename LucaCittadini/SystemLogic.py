
# TODO don't forget what classes are, they consist of attributes and methods, not just lines of code to be executed like "print()"

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
        global rangeSense
        global movPhase
        global forkFlag
        global pickDropFlag
        global mergeFlag
        global turnOne
        global turnTwo
        global pickUpSideOne
        global pickUpSideTwo
        global motorInstruc
        global pwmA
        global pwmB
        global startTime    

        phaseA: int = 6
        enableA: int = 13
        phaseB: int = 19
        enableB: int = 26
        smallServoCtrl: int = 5
        largeServoCtrl: int = 0
        rangeSense: int = 2
        movPhase: str = 'phaseFork'
        forkFlag: bool = False
        pickDropFlag: bool = False
        mergeFlag: bool = False

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(phaseA, GPIO.OUT)
        GPIO.setup(enableA, GPIO.OUT) 
        GPIO.setup(phaseB, GPIO.OUT)
        GPIO.setup(enableB, GPIO.OUT) 
        GPIO.setup(largeServoCtrl, GPIO.OUT) 
        GPIO.setup(smallServoCtrl, GPIO.OUT) 
        GPIO.setup(rangeSense, GPIO.IN) 
        
        GPIO.output(phaseA, GPIO.LOW)
        GPIO.output(enableA, GPIO.LOW)
        GPIO.output(phaseB, GPIO.LOW)
        GPIO.output(enableB, GPIO.LOW)

        pwmA = GPIO.PWM(enableA, 1000)
        pwmB = GPIO.PWM(enableB, 1000)
        pwmA.start(0)
        pwmB.start(0)

    def switch(self, sav) -> None:
        self.state.switch(self)
        
class IDLE:
    def userWait() -> None: 
        while(True):        
            match input('Type "Start" to begin program when you\'re ready: \n').lower():
                case 's' | 'start':
                    break
                case _:
                    print('Invalid, try again. \n')
    
    def switch(self, sav) -> None:
        sav.state = LISTENING()
        print('Changing state to LISTENING')

class LISTENING:
    def findPath() -> None:
        TParray: list[bool] = MV() 
        turnOne: bool = TParray(0)
        pickUpSideOne: bool = TParray(1)
        turnTwo: bool = TParray(2)
        pickUpSideTwo: bool = TParray(3)

    def userWait() -> None:
        while(True):
            match input('Decisions received, type "Next" to start race: \n').lower():
                case 'n' | 'next':
                    break
                case _:
                    print('Invalid, try again. \n')

    def startStopWatch() -> None: # Move into userWait() method?
        startTime: float = time()

    def switch(self, sav) -> None:
        sav.state = MOVING()
        print('Changing state to MOVING')

class MOVING:
    def driving() -> None:
        while(True): 
            rangeOut = bool(GPIO.input(rangeSense))
            if movPhase == 'phasePickDrop' | 'phasePark':
                if rangeOut == True:
                    GPIO.output(phaseA, 0)
                    pwmA.ChangeDutyCycle(0)
                    GPIO.output(phaseB, 0)
                    pwmB.ChangeDutyCycle(0)
                    break
                else:
                    motorInstruc = FindCase()
                    GPIO.output(phaseA, motorInstruc(0))
                    pwmA.ChangeDutyCycle(motorInstruc(1))
                    GPIO.output(phaseB, motorInstruc(2))
                    pwmB.ChangeDutyCycle(motorInstruc(3))
            else:
                motorInstruc = FindCase()
                GPIO.output(phaseA, motorInstruc(0))
                pwmA.ChangeDutyCycle(motorInstruc(1))
                GPIO.output(phaseB, motorInstruc(2))
                pwmB.ChangeDutyCycle(motorInstruc(3))
    
    def switch(self, sav) -> None:
        match movPhase:
            case 'phasePickDrop':
                if pickDropFlag == False:
                    sav.state = PICKUP()
                    print('Changing state to PICKUP')
                else:
                    sav.state = DROPOFF()
                    print('Changing state to DROPOFF')
            case 'phasePark':
                sav.state = PARKING()
                print('Changing state to PARKING')

class PICKUP:
    # NOTE Should at some point indicate that this state has been jumped to so that sav moves to the next MOVING phase
    # Should stop the sav (send data to the motor driver)
    # Potentially change motor driver mode
    # Potentially fix position (to ensure it picks up in right place)
    # Send data to large servo (some function, will need to go up and down)
    # Send data to small servo (some function)
    def switch(self, sav) -> None:
        sav.state = MOVING()
        print('Changing state to MOVING')

class DROPOFF:
    # Essentially it needs to complete the same task in PICKUP but maybe a different order or values
    def switch(self, sav) -> None:
        sav.state = MOVING()
        print('Changing state to MOVING')

class PARKING:
    # Should stop, re-adjust if needed 
    # NOTE not sure if any other tasks need to be complete during this state
    def switch(self, sav) -> None:
        sav.state = COMPLETE()
        print('Changing state to COMPLETE')

class COMPLETE:
    def endStopWatch() -> None:
        endTime: float = time()
        raceTime: float = endTime - startTime
        minutes: int = raceTime//60
        seconds: float = raceTime%60
        print('You took %d minutes and %f seconds to complete the track. ' % (minutes, seconds))

    def clean():
        GPIO.cleanup()
    
    def switch(self, sav) -> None:
        ...
    
    # End programme nicely (stop processes and other programmes, have a nice complete message at the end)

def main() -> None:
    sav = SAV()
    sav.userWait()
    sav.switch() # Move to LISTENING state

    sav.findPath()
    sav.userWait()
    sav.startStopWatch()
    sav.switch() # Move to MOVING state

    sav.driving()
    sav.switch() # Move to PARKING state
    
