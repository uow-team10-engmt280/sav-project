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
        # global motorDriverMode
        global turnOne
        global turnTwo
        global pickUpSideOne
        global pickUpSideTwo
        global motorInstruc
        global pwmA
        global pwmB


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
        # motorDriverMode: bool = False

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
    print('Entered LISTENING state successfully. \n')

    TParray: list[bool] = MV() 
    turnOne: bool = TParray(0)
    pickUpSideOne: bool = TParray(1)
    turnTwo: bool = TParray(2)
    pickUpSideTwo: bool = TParray(3)
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
        print('Changing state')

class MOVING:
    print('Entered MOVING state successfully. \n')
    def driving():
        while(True): 
            rangeOut = bool(GPIO.input(rangeSense))
            if movPhase == 'phasePickDrop' | 'phasePark':
                if rangeOut == True:
                    GPIO.output(phaseA, 0)
                    pwmA.ChangeDutyCycle(0)
                    GPIO.output(phaseB, 0)
                    pwmB.ChangeDutyCycle(0)
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
                


    # Sends the decision to the motor driver to turn the sav accordingly
    
    if pickDropFlag == False:
        def switch(self, sav) -> None:
            sav.state = PICKUP()
            print('Changing to state PICKUP')
    else:
        def switch(self, sav) -> None:
            sav.state = DROPOFF()
            print('Changing to state DROPOFF')

class PICKUP:
    print('Entered PICKUP state successfully. \n')
    # NOTE Should at some point indicate that this state has been jumped to so that sav moves to the next MOVING phase
    # Should stop the sav (send data to the motor driver)
    # Potentially change motor driver mode
    # Potentially fix position (to ensure it picks up in right place)
    # Send data to large servo (some function, will need to go up and down)
    # Send data to small servo (some function)
    def switch(self, sav) -> None:
        sav.state = MOVING()
        print('Changing state')

class DROPOFF:
    print('Entered DROPOFF state successfully. \n')
    # Essentially it needs to complete the same task in PICKUP but maybe a different order or values
    def switch(self, sav) -> None:
        sav.state = MOVING()
        print('Changing state')

class PARKING:
    print('Entered PARKING state successfully. \n')
    # Should stop, re-adjust if needed 
    # NOTE not sure if any other tasks need to be complete during this state
    def switch(self, sav) -> None:
        sav.state = COMPLETE()
        print('Changing state')

class COMPLETE:
    print('Entered COMPLETE state successfully.')
    endTime: float = time()
    raceTime: float = endTime - startTime
    minutes: int = raceTime//60
    seconds: float = raceTime%60
    print('You took %d minutes and %f seconds to complete the track. ' % (minutes, seconds))

    GPIO.cleanup()
    # End programme nicely (stop processes and other programmes, have a nice complete message at the end)

def main() -> None:
    ...
