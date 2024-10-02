import RPi.GPIO as GPIO # type: ignore 
import time as t

def getSensorArray() -> None:
    GPIO.setmode(GPIO.BCM)
    pins: list = [11, 5, 9, 10, 14, 22, 15, 6] 
    firstSensorTime: float = t.time()
    try:
    
        timings: list[float] = [] 
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
        timings(0) = timings(0) - firstSensorTime 
        print(timings)
    finally:
        GPIO.cleanup()

getSensorArray()