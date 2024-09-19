from time import sleep, time
# from SystemLogic import pwmSmall, pwmLarge, smallServoCtrl, largeServoCtrl
import RPi.GPIO as GPIO # type: ignore

# NOTE Small servo angles go between 0 and 120 degrees, Large servo angles from 0 to 180 degrees
# The small servo pulse widths go from 900µs to 2100µs (0.9ms, 2.1ms)
# The large servo pulse widths go from 500µs to 2500µs (0.5ms, 2.5ms)


def setSmallServo(angle: int) -> None:
    dutyCycle: float = 4.5 + (angle / 120) * 6
    pwmSmall.ChangeDutyCycle(dutyCycle)
    sleep(2)
    pwmSmall.stop()

def setLargeServo(angle: int) -> None:
    dutyCycle: float = 2.5 + (angle / 180) * 10
    pwmLarge.ChangeDutyCycle(dutyCycle)
    sleep(2)
    pwmLarge.stop()



def testServos() -> None:
    global pwmSmall
    global pwmLarge

    smallServoCtrl: int = 5
    largeServoCtrl: int = 0
    GPIO.setup(largeServoCtrl, GPIO.OUT) 
    GPIO.setup(smallServoCtrl, GPIO.OUT) 
    pwmSmall = GPIO.PWM(smallServoCtrl, 50)
    pwmLarge = GPIO.PWM(largeServoCtrl, 50) 
    pwmSmall.start(0) 
    pwmLarge.start(0) 

    setSmallServo(0)
    sleep(3)
    setSmallServo(60)
    sleep(3)
    setSmallServo(0)
    sleep(3)
    setSmallServo(120)
    sleep(4)
    setLargeServo(0)
    sleep(3)
    setLargeServo(45)
    sleep(2)
    setLargeServo(90)
    sleep(2)
    setLargeServo(180)
    sleep(2)
    setLargeServo(135)
    sleep(2)
    setLargeServo(90)

    print("Testing Complete.")

testServos()


# def artiPWM():
#     while True:
#         GPIO.output(smallServoCtrl, GPIO.LOW)
#         sleep(1/104.5)
#         GPIO.output(smallServoCtrl, GPIO.HIGH)
#         sleep(1/104.5)