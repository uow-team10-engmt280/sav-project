from time import sleep, time
from SystemLogic import pwmSmall, pwmLarge, smallServoCtrl, largeServoCtrl
import RPi.GPIO as GPIO # type: ignore

# NOTE Small servo angles go between 0 and 120 degrees, Large servo angles from 0 to 180 degrees
# The small servo pulse widths go from 900µs to 2100µs (0.9ms, 2.1ms)
# The large servo pulse widths go from 500µs to 2500µs (0.5ms, 2.5ms)
# TODO MAY HAVE TO ARTIFICIALLY CREATE PWMs

# CODE FOR ARTIFICIAL PWMS:
# NOTE we want a frequency of 50, that means 50 full cycles in a second, so
test = 0
startTime = time()
while test < 50:
    GPIO.output(smallServoCtrl, GPIO.LOW)
    sleep(1/104.5)
    GPIO.output(smallServoCtrl, GPIO.HIGH)
    sleep(1/104.5)
endTime = time()

print(startTime - endTime)
print(test)

# def setSmallServo(angle: int) -> None:
#     dutyCycle: float = 4.5 + (angle / 120) * 6
#     pwmSmall.ChangeDutyCycle(dutyCycle)
#     sleep(2)
#     pwmSmall.ChangeDutyCycle(0)

# def setLargeServo(angle: int) -> None:
#     dutyCycle: float = 2.5 + (angle / 180) * 10
#     pwmLarge.ChangeDutyCycle(dutyCycle)
#     sleep(2)
#     pwmLarge.ChangeDutyCycle(0)
