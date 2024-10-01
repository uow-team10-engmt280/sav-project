# from RPi import GPIO # type: ignore 
# import time
# import SOME_ARRAY # type: ignore
from typing import Protocol
# from MachineVisionLuca import MV, takePicture
# from FindCase import FindCase
# from ServoFunctions import setLargeServo, setSmallServo

class State(Protocol):
    def switch(self, state) -> None:
        ...

class SAV:
    
    def __init__(self, state):
        self.state = state

        # self.phaseA: int = 5
        # self.enableA: int = 12
        # self.phaseB: int = 19
        # self.enableB: int = 13

        # self.smallServoCtrl: int = 16
        # self.largeServoCtrl: int = 21

        # self.rangeSense: int = 6
        # self.movPhase: str = 'phaseFork'
        # self.forkFlag: bool = False
        # self.pickDropFlag: bool = False
        # self.mergeFlag: bool = False

        # GPIO.setmode(GPIO.BCM)

        # GPIO.setup(self.phaseA, GPIO.OUT)
        # GPIO.setup(self.enableA, GPIO.OUT) 
        # GPIO.setup(self.phaseB, GPIO.OUT)
        # GPIO.setup(self.enableB, GPIO.OUT) 
        # GPIO.setup(self.largeServoCtrl, GPIO.OUT) 
        # GPIO.setup(self.smallServoCtrl, GPIO.OUT) 
        # GPIO.setup(self.rangeSense, GPIO.IN) 
        
        # GPIO.output(self.phaseA, GPIO.LOW)
        # GPIO.output(self.enableA, GPIO.LOW)
        # GPIO.output(self.phaseB, GPIO.LOW)
        # GPIO.output(self.enableB, GPIO.LOW)

        # self.pwmA = GPIO.PWM(self.enableA, 1000)
        # self.pwmB = GPIO.PWM(self.enableB, 1000)
        # self.pwmSmall = GPIO.PWM(self.smallServoCtrl, 50)
        # self.pwmLarge = GPIO.PWM(self.largeServoCtrl, 50) 
        # self.pwmA.start(0)
        # self.pwmB.start(0)
        # self.pwmSmall.start(0) 
        # self.pwmLarge.start(0) 

    def switch(self) -> None:
        self.state.switch(self) # FIXME What does this do exactly?
        
class IDLE:

    def __init__(self, state) -> None:
        self.state = state

    def userWait(self) -> None: 
        while(True):        
            match input('Type "Start" to begin programme when you\'re ready: \n').lower():
                case 's' | 'start':
                    break
                case _:
                    print('Invalid, try again. \n')
    
    def switch(self, sav) -> None:
        self.sav.state = LISTENING()
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
        self.sav.state = MOVING()
        print('Changing state to MOVING')

class MOVING:

    def driving(self) -> None:

        while(True): 
            self.rangeOut = bool(GPIO.input(self.rangeSense))
            if self.movPhase == 'phasePickDrop' | 'phasePark':
                if self.rangeOut == True:
                    GPIO.output(self.phaseA, 0)
                    self.pwmA.ChangeDutyCycle(0)
                    GPIO.output(self.phaseB, 0)
                    self.pwmB.ChangeDutyCycle(0)
                    break
                else:
                    self.motorInstruc: list[any] = FindCase(SOME_ARRAY) # FIXME
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
                    self.sav.state = PICKUP()
                    print('Changing state to PICKUP')
                else:
                    self.sav.state = DROPOFF()
                    print('Changing state to DROPOFF')
            case 'phasePark':
                self.sav.state = PARKING()
                print('Changing state to PARKING')

class PICKUP: 
    movPhase: str = 'phaseMerge'
    pickDropFlag: bool = True 

    def reverse(self) -> None:
        self.reverseTime = time.time()
        while True:
            GPIO.output(self.phaseA, 0)
            self.pwmA.ChangeDutyCycle(50/1000) # The divide by thousand is because of the frequency
            GPIO.output(self.phaseB, 0)
            self.pwmB.ChangeDutyCycle(50/1000)
            if self.reverseTime - time.time() == 3:
                break

    def pickUpLegoMan(self) -> None: # FIXME check the note in the ServoFunctions programme
        self.pwmSmall.start(0) 
        self.pwmLarge.start(0) 
        setSmallServo(180)
        time.sleep(1)
        if self.pickUpSide == False:
            setLargeServo(0) 
        else:
            setLargeServo(180)
        time.sleep(1)
        setSmallServo(45)
        time.sleep(1)
        setLargeServo(90)
        time.sleep(1)
        self.pwmSmall.stop(0) 
        self.pwmLarge.stop(0) 

    def switch(self, sav) -> None:
        sav.state = MOVING()
        print('Changing state to MOVING')

class DROPOFF:

    movPhase: str = 'phaseMerge'
    def dropOffLegoMan(self) -> None: # FIXME check the note in the ServoFunctions programme
        self.pwmSmall.start(0) 
        self.pwmLarge.start(0) 
        if self.dropOffSide == False:
            setLargeServo(0)
        else: 
            setLargeServo(180)
        time.sleep(1)
        setSmallServo(180)
        time.sleep(1)
        setLargeServo(90)
        time.sleep(1)
        setSmallServo(45) # Actually 0 but function wrong
        time.sleep(1)
        self.pwmSmall.stop(0) 
        self.pwmLarge.stop(0) 

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

