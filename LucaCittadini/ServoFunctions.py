from time import sleep, time
from SystemLogic import SAV
import RPi.GPIO as GPIO # type: ignore

# NOTE Small servo angles go between 0 and 120 degrees, Large servo angles from 0 to 180 degrees
# The small servo pulse widths go from 900µs to 2100µs (0.9ms, 2.1ms)
# The large servo pulse widths go from 500µs to 2500µs (0.5ms, 2.5ms)

# NOTE 0 degrees is fully to the right, 120 and 180 are fully to the left for the small and large servos respectively

def setSmallServo(angle: int) -> None:
    dutyCycle: float = 6.5 + (angle / 120) * 7 # should test
    SAV.pwmSmall.ChangeDutyCycle(dutyCycle)

def setLargeServo(angle: int) -> None:
    dutyCycle: float = 2.5 + (angle / 180) * 10 # good
    SAV.pwmLarge.ChangeDutyCycle(dutyCycle)

# def testServos() -> None:
#     GPIO.setmode(GPIO.BCM)
#     global pwmSmall
#     global pwmLarge

#     smallServoCtrl: int = 5 
#     largeServoCtrl: int = 0
#     GPIO.setup(largeServoCtrl, GPIO.OUT) 
#     GPIO.setup(smallServoCtrl, GPIO.OUT) 
#     pwmSmall = GPIO.PWM(smallServoCtrl, 50)
#     pwmLarge = GPIO.PWM(largeServoCtrl, 50) 
#     pwmSmall.start(0) 
#     pwmLarge.start(0) 

#     setSmallServo(0)
#     sleep(3)
#     setSmallServo(60)
#     sleep(3)
#     setSmallServo(0)
#     sleep(3)
#     setSmallServo(120)
#     sleep(4)
#     setLargeServo(0)
#     sleep(3)
#     setLargeServo(45)
#     sleep(2)
#     setLargeServo(90)
#     sleep(2)
#     setLargeServo(180)
#     sleep(2)
#     setLargeServo(135)
#     sleep(2)
#     setLargeServo(90)
#     GPIO.cleanup()

#     print("Testing Complete.")