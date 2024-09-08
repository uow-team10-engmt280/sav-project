
# TODO don't forget what classes are, they consist of attributes and methods, not just lines of code to be executed like "print()"

import RPi.GPIO as GPIO # type: ignore 
import time
from typing import Protocol
from MachineVisionMain import MV 
from FindCase import FindCase
from ServoFunctions import setLargeServo, setSmallServo

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
        global pickUpSide
        global dropOffSide
        global motorInstruc
        global pwmA
        global pwmB
        global pwmSmall
        global pwmLarge
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
        pwmSmall = GPIO.PWM(smallServoCtrl, 50) 
        pwmLarge = GPIO.PWM(smallServoCtrl, 50)
        pwmA.start(0)
        pwmB.start(0)
        pwmSmall.start(0) 
        pwmLarge.start(0)

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
        pickUpSide: bool = TParray(1)
        turnTwo: bool = TParray(2)
        dropOffSide: bool = TParray(3)

    def userWait() -> None:
        while(True):
            match input('Decisions received, type "Next" to start race: \n').lower():
                case 'n' | 'next':
                    break
                case _:
                    print('Invalid, try again. \n')

    def startStopWatch() -> None: # Move into userWait() method?
        startTime: float = time.time()

    def switch(self, sav) -> None:
        sav.state = MOVING()
        print('Changing state to MOVING')

class MOVING:

    def driving() -> None:
        while(True): 
            rangeOut = bool(GPIO.input(rangeSense))
            if movPhase == 'phasePickDrop' | 'phasePark': # We are only listening to the range sensor if we are in these phases
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
    # Potentially fix position (to ensure it picks up in right place)
    #   - Check reflect sensor to see if we are in middle of the track
    #   - If it doesn't return [0, 0, 0, 1, 1, 1, 0, 0, 0] then fix position
    movPhase: str = 'phaseMerge'
    def pickUpLegoMan() -> None:
        setSmallServo(120) # These may need to switch
        time.sleep(2)
        if pickUpSide == False:
            setLargeServo(180) # These may need to switch
        else:
            setLargeServo(0)
        time.sleep(2)
        setSmallServo(0)
        time.sleep(2)
        setLargeServo(90)
        time.sleep(2)

    def switch(self, sav) -> None:
        sav.state = MOVING()
        print('Changing state to MOVING')

class DROPOFF:
    movPhase: str = 'phaseMerge'
    def dropOffLegoMan() -> None:
        if dropOffSide == False:
            setLargeServo(180)
        else: 
            setLargeServo(0)
        time.sleep(2)
        setSmallServo(120)
        time.sleep(2)
        setLargeServo(90)
        time.sleep(2)
        setSmallServo(0)
        time.sleep(2)

    def switch(self, sav) -> None:
        sav.state = MOVING()
        print('Changing state to MOVING')

class PARKING:

    def parkSAV() -> None:
        ...
    # NOTE not sure if any other tasks need to be complete during this state
    def switch(self, sav) -> None:
        sav.state = COMPLETE()
        print('Changing state to COMPLETE')

class COMPLETE:
    def endStopWatch() -> None:
        endTime: float = time.time()
        raceTime: float = endTime - startTime
        minutes: int = raceTime//60
        seconds: float = raceTime%60
        print('You took %d minutes and %f seconds to complete the track. ' % (minutes, seconds))

    def clean() -> None:
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
    sav.switch() # Move to PICKUP state

    sav.pickUpLegoMan()
    sav.switch() # Move to MOVING state

    sav.driving()
    sav.switch() # Move to DROPOFF state

    sav.dropOffLegoMan()
    sav.switch() # Move to MOVING state

    sav.driving()
    sav.switch() # Move to PARKING state

    sav.parkSAV()
    sav.switch() # Move to COMPLETE state

    sav.endStopWatch()
    sav.clean()

    
