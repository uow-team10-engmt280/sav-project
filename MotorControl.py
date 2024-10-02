from RPi import GPIO # type: ignore

class Motor:

    def __init__(self, ePin, pPin) -> None:
        GPIO.setmode(GPIO.BCM)
        self.enablePin = ePin
        self.phasePin = pPin

