from time import sleep
from SystemLogic import pwmSmall, pwmLarge

# NOTE Small servo angles go between 0 and 120 degrees, Large servo angles from 0 to 180 degrees
# The small servo pulse widths go from 900µs to 2100µs3 (0.9ms, 2.1ms)
# The large servo pulse widths go from 500µs to 2500µs  (0.5ms, 2.5ms)

def setSmallServo(angle: int) -> None:
    dutyCycle: float = 4.5 + (angle / 120) * 6
    pwmSmall.ChangeDutyCycle(dutyCycle)
    sleep(2)
    pwmSmall.ChangeDutyCycle(0)

def setLargeServo(angle: int) -> None:
    dutyCycle: float = 2.5 + (angle / 180) * 10
    pwmLarge.ChangeDutyCycle(dutyCycle)
    sleep(2)
    pwmLarge.ChangeDutyCycle(0)
