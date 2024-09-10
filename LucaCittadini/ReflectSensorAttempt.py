# REGULAR VERSION
import RPi.GPIO as GPIO # type: ignore 
import time as t


def getSensorArrayV1():
    pin1: int = 23
    pin2: int = 20
    pin3: int = 24
    pin4: int = 16
    pin5: int = 25
    pin6: int = 12
    pin7: int = 8
    pin8: int = 1
    pin9: int = 7

    pins: tuple = (pin1, pin2, pin3, pin4, pin5, pin6, pin7, pin8, pin9)

    while(True):
        GPIO.setmode(GPIO.BCM)
        for pin1 in pins:
            GPIO.setup(pin1, GPIO.OUT)
            GPIO.output(pin1, GPIO.LOW)
        timings: list[float] = []
        testTime1: float = t.time()
        for pin1 in pins:
            GPIO.setup(pin1, GPIO.OUT)
            GPIO.output(pin1, GPIO.HIGH)
            GPIO.setup(pin1, GPIO.IN)
            startTime: float = t.time()
            while(True):
                if bool(GPIO.input(pin1)) == True:
                    pass
                else:
                    break
            endTime: float = t.time()
            timingValue: float = endTime - startTime
            timings.append(timingValue)
        testTime2: float = t.time()
        findArrayTime: float = testTime2 - testTime1
        print(timings)
        print(f'It takes {findArrayTime} seconds to find 1 array of timing values for the reflectance sensor')
        GPIO.cleanup()

