import RPi.GPIO as GPIO # type: ignore 
import time as t

def getSensorArrayV1() -> None:
    GPIO.setmode(GPIO.BCM)
    pins: list = [11, 5, 9, 10, 14, 22, 15, 6] 
    firstSensorTime: float = t.time()
    try:
        while(True):
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
    except:
        print('We\'ve had an error, please check your main while loop')
    GPIO.cleanup()

getSensorArrayV1()