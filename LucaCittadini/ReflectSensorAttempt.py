import RPi.GPIO as GPIO # type: ignore 
import time as t


def getSensorArrayV1() -> None:
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
    negateTime: float = t.time()
    try:
        while(True):
            GPIO.setmode(GPIO.BCM)
            timings: list[float] = [] # FIXME
# testTime1: float = t.time()
            for pin in pins:
                GPIO.setup(pin, GPIO.OUT)
                GPIO.output(pin, GPIO.HIGH)
                GPIO.setup(pin, GPIO.IN)
                startTime: float = t.time() 
                while(True):
                    if GPIO.input(pin) == False:
                        break
                endTime: float = t.time()
                timingValue: float = endTime - startTime
                timings.append(timingValue)
            timings(0) = timings(0) - negateTime 
# testTime2: float = t.time()
# findArrayTime: float = testTime2 - testTime1
            print(timings)
# print(f'It takes {findArrayTime} seconds to find 1 array of timing values for the reflectance sensor')
            GPIO.cleanup()
    except:
        print('We\'ve had an error, please check your main while loop')

