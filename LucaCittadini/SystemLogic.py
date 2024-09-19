import RPi.GPIO as GPIO # type: ignore 
import time
import SOME_ARRAY # type: ignore
from typing import Protocol
from MachineVisionLuca import MV 
from FindCase import FindCase
from ServoFunctions import setLargeServo, setSmallServo
from FixPosition import fixPosition

class State(Protocol):
    def switch(self, sav) -> None:
        ...


class SAV:
    
    def __init__(self):
        self.state = IDLE()
        # FIXME might have to move "global"s out of method
        global phaseA
        global enableA
        global phaseB
        global enableB
        global rangeSense
        global movPhase
        global forkFlag
        global pickDropFlag
        global mergeFlag
        global pwmA
        global pwmB
        global pwmSmall
        global pwmLarge

        phaseA: int = 6
        enableA: int = 13
        phaseB: int = 19
        enableB: int = 26
        rangeSense: int = 2
        movPhase: str = 'phaseFork'
        smallServoCtrl: int = 5
        largeServoCtrl: int = 0
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
        pwmLarge = GPIO.PWM(largeServoCtrl, 50) 
        pwmA.start(0)
        pwmB.start(0)
        pwmSmall.start(0) 
        pwmLarge.start(0) 

    def switch(self) -> None:
        self.state.switch(self) # FIXME What does this do exactly?
        
class IDLE:

    def userWait(self) -> None: 
        while(True):        
            match input('Type "Start" to begin programme when you\'re ready: \n').lower():
                case 's' | 'start':
                    break
                case _:
                    print('Invalid, try again. \n')
    
    def switch(self, sav) -> None:
        sav.state = LISTENING()
        print('Changing state to LISTENING')

class LISTENING:

    def findPath(self) -> None:
        global turnOne
        global turnTwo
        global pickUpSide
        global dropOffSide
        TParray: list[bool] = MV()
        turnOne: bool = TParray(0)
        pickUpSide: bool = TParray(1)
        turnTwo: bool = TParray(2)
        dropOffSide: bool = TParray(3)

    def userWait(self) -> None:
        while(True):
            match input('Decisions received, type "Next" to start race: \n').lower():
                case 'n' | 'next':
                    break
                case _:
                    print('Invalid, try again. \n')

    def startStopWatch(self) -> None: # Move into userWait() method?
        global startTime
        startTime: float = time.time()

    def switch(self, sav) -> None:
        sav.state = MOVING()
        print('Changing state to MOVING')

class MOVING:

    def driving(self) -> None:
        while(True): 
            global rangeOut
            rangeOut = bool(GPIO.input(rangeSense))
            if movPhase == 'phasePickDrop' | 'phasePark': 
                if rangeOut == True:
                    GPIO.output(phaseA, 0)
                    pwmA.ChangeDutyCycle(0)
                    GPIO.output(phaseB, 0)
                    pwmB.ChangeDutyCycle(0)
                    break
                else:
                    motorInstruc = FindCase(SOME_ARRAY) # FIXME
                    GPIO.output(phaseA, motorInstruc(0))
                    pwmA.ChangeDutyCycle(motorInstruc(1)) 
                    GPIO.output(phaseB, motorInstruc(2))
                    pwmB.ChangeDutyCycle(motorInstruc(3))
            else:
                motorInstruc = FindCase(SOME_ARRAY) # FIXME
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
    movPhase: str = 'phaseMerge'
    pickDropFlag: bool = True 

    # def checkPos(self) -> None: 
    #     if SOME_ARRAY == [0, 0, 0, 1, 1, 1, 0, 0, 0]:
    #         ... 
    #     else:
    #         fixPosition() # This will call some function that makes the SAV move to fix it's position
    def pickUpLegoMan(self) -> None:
        setSmallServo(120)
        time.sleep(2)
        if pickUpSide == False:
            setLargeServo(180) 
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
    def dropOffLegoMan(self) -> None:
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

    def parkSAV(self) -> None: # TODO
        ...

    def switch(self, sav) -> None:
        sav.state = COMPLETE()
        print('Changing state to COMPLETE')

class COMPLETE:

    def endStopWatch(self) -> None:
        endTime: float = time.time()
        raceTime: float = endTime - startTime
        minutes: int = raceTime//60
        seconds: float = raceTime%60
        print(f'You took {minutes} minutes and {seconds} seconds to complete the track. ')

    def clean(self) -> None:
        GPIO.cleanup()
    
    def switch(self, sav) -> None:
        ...
    
    # End programme nicely (stop processes and other programmes, have a nice complete message at the end)

def main() -> None:
    sav = SAV()
    sav.__init__()
    sav.switch() # Not sure about this, is it needed?

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

    
