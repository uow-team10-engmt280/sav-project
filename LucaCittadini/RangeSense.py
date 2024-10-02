from RPi import GPIO # type: ignore

def detect() -> None:
    GPIO.setmode(GPIO.BCM)
    rangeSensor = 6
    GPIO.setup(rangeSensor, GPIO.IN)
    return not bool(GPIO.input(rangeSensor))