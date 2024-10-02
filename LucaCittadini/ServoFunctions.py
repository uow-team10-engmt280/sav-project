# PERFECT (needs testing however)

from time import sleep
import RPi.GPIO as GPIO # type: ignore

def initServos(function): # The decorator
    def wrapper(*args, **kwargs):
        GPIO.setmode(GPIO.BCM)
        smallServoCtrl = 25
        largeServoCtrl = 21
        GPIO.setup(smallServoCtrl, GPIO.OUT) 
        GPIO.setup(largeServoCtrl, GPIO.OUT) 
        pwmS = GPIO.PWM(smallServoCtrl, 50)
        pwmL = GPIO.PWM(largeServoCtrl, 50)
        return function(*args, **kwargs, pwmS, pwmL)
    return wrapper


def setSmallServo(angle, pwmS=None) -> None:
    pwmS.start(0)
    dutyCycle: float = 6.5 + (angle / 120) * 7 # should test
    pwmS.ChangeDutyCycle(dutyCycle) 
    sleep(2)
    pwmS.stop()


def setLargeServo(angle, pwmL=None) -> None:
    pwmL.start(0)
    dutyCycle: float = 2.5 + (angle / 180) * 10 # good
    pwmL.ChangeDutyCycle(dutyCycle) # going to need to change this, probably just directly refer to the pins
    sleep(2)
    pwmL.stop()

def pickUpLeft(pwmS=None, pwmL=None) -> None:
    setSmallServo(120, pwmS)
    setLargeServo(0, pwmL)
    setSmallServo(20, pwmS)
    setLargeServo(90, pwmL)

def pickUpRight(pwmS=None, pwmL=None) -> None:
    setSmallServo(120, pwmS)
    setLargeServo(180, pwmL)
    setSmallServo(20, pwmS)
    setLargeServo(90, pwmL)

def dropOffLeft(pwmS=None, pwmL=None) -> None:
    setLargeServo(0, pwmL)
    setSmallServo(120, pwmS)
    setLargeServo(90, pwmL)
    setSmallServo(20, pwmS)

def dropOffRight(pwmS=None, pwmL=None) -> None:
    setLargeServo(180, pwmL)
    setSmallServo(120, pwmS)
    setLargeServo(90, pwmL)
    setSmallServo(20, pwmS)

@initServos
def servoAction(turn, side, pwmS=None, pwmL=None) -> None:
    try:
        match turn:
            case False:
                match side:
                    case False:
                        pickUpLeft(pwmS, pwmL)
                    case True:
                        pickUpRight(pwmS, pwmL)
            case True:
                match side:
                    case False:
                        dropOffLeft(pwmS, pwmL)
                    case True:
                        dropOffRight(pwmS, pwmL)
    finally:
        GPIO.cleanup()
