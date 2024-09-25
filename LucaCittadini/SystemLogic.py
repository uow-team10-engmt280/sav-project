from RPi import GPIO # type: ignore 
import time
import SOME_ARRAY # type: ignore
from typing import Protocol
from MachineVisionLuca import MV, takePicture
from FindCase import FindCase
from ServoFunctions import setLargeServo, setSmallServo

class State(Protocol):
    def switch(self, sav) -> None:
        ...

class SAV:
    
    def __init__(self):
        self.state = IDLE()

        self.phaseA: int = 5
        self.enableA: int = 12
        self.phaseB: int = 19
        self.enableB: int = 13

        self.smallServoCtrl: int = 16
        self.largeServoCtrl: int = 21

        self.rangeSense: int = 6
        self.movPhase: str = 'phaseFork'
        self.forkFlag: bool = False
        self.pickDropFlag: bool = False
        self.mergeFlag: bool = False

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.phaseA, GPIO.OUT)
        GPIO.setup(self.enableA, GPIO.OUT) 
        GPIO.setup(self.phaseB, GPIO.OUT)
        GPIO.setup(self.enableB, GPIO.OUT) 
        GPIO.setup(self.largeServoCtrl, GPIO.OUT) 
        GPIO.setup(self.smallServoCtrl, GPIO.OUT) 
        GPIO.setup(self.rangeSense, GPIO.IN) 
        
        GPIO.output(self.phaseA, GPIO.LOW)
        GPIO.output(self.enableA, GPIO.LOW)
        GPIO.output(self.phaseB, GPIO.LOW)
        GPIO.output(self.enableB, GPIO.LOW)

        self.pwmA = GPIO.PWM(self.enableA, 1000)
        self.pwmB = GPIO.PWM(self.enableB, 1000)
        self.pwmSmall = GPIO.PWM(self.smallServoCtrl, 50)
        self.pwmLarge = GPIO.PWM(self.largeServoCtrl, 50) 
        self.pwmA.start(0)
        self.pwmB.start(0)
        self.pwmSmall.start(0) 
        self.pwmLarge.start(0) 

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

        takePicture()

        

        self.TParray: list[bool] = MV()
        self.turnOne: bool = self.TParray(0)
        self.pickUpSide: bool = self.TParray(1)
        self.turnTwo: bool = self.TParray(2)
        self.dropOffSide: bool = self.TParray(3)

    def userWait(self) -> None:
        while(True):
            match input('Decisions received, type "Next" to start race: \n').lower():
                case 'n' | 'next':
                    self.startTime: float = time.time()
                    break
                case _:
                    print('Invalid, try again. \n')

    def switch(self, sav) -> None:
        sav.state = MOVING()
        print('Changing state to MOVING')

class MOVING:

    def driving(self) -> None:

        while(True): 
            rangeOut = bool(GPIO.input(self.rangeSense))
            if self.movPhase == 'phasePickDrop' | 'phasePark':
                if rangeOut == True:
                    GPIO.output(self.phaseA, 0)
                    self.pwmA.ChangeDutyCycle(0)
                    GPIO.output(self.phaseB, 0)
                    self.pwmB.ChangeDutyCycle(0)
                    break
                else:
                    motorInstruc: list[any] = FindCase(SOME_ARRAY) # FIXME
                    GPIO.output(self.phaseA, motorInstruc(0))
                    self.pwmA.ChangeDutyCycle(motorInstruc(1)/1000) # The divide by thousand is because of the frequency
                    GPIO.output(self.phaseB, motorInstruc(2))
                    self.pwmB.ChangeDutyCycle(motorInstruc(3)/1000)
            else:
                motorInstruc: list[any] = FindCase(SOME_ARRAY) # FIXME
                GPIO.output(self.phaseA, motorInstruc(0))
                self.pwmA.ChangeDutyCycle(motorInstruc(1)/1000)
                GPIO.output(self.phaseB, motorInstruc(2))
                self.pwmB.ChangeDutyCycle(motorInstruc(3)/1000)

    def switch(self, sav) -> None:
        match self.movPhase:
            case 'phasePickDrop':
                if self.pickDropFlag == False:
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

    # TODO add method to move backwards so that arm is inline
    def reverse(self) -> None:
        reverseTime = time.time()
        while True:
            GPIO.output(self.phaseA, 0)
            self.pwmA.ChangeDutyCycle(50/1000) # The divide by thousand is because of the frequency
            GPIO.output(self.phaseB, 0)
            self.pwmB.ChangeDutyCycle(50/1000)
            if reverseTime - time.time() == 3:
                break

    def pickUpLegoMan(self) -> None: # FIXME check the note in the ServoFunctions programme
        setSmallServo(120)
        time.sleep(2)
        if self.pickUpSide == False:
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
    def dropOffLegoMan(self) -> None: # FIXME check the note in the ServoFunctions programme
        if self.dropOffSide == False:
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

    def reverse(self) -> None:
        reverseTime = time.time()
        while True:
            GPIO.output(self.phaseA, 0)
            self.pwmA.ChangeDutyCycle(50/1000) # The divide by thousand is because of the frequency
            GPIO.output(self.phaseB, 0)
            self.pwmB.ChangeDutyCycle(50/1000)
            if reverseTime - time.time() == 3:
                break

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
        raceTime: float = endTime - self.startTime
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

    
