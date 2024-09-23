
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# list of pins corresponding to reflectance sensor output lines
pins = [11, 17, 9, 4, 10, 14, 22, 15, 27]

# initialise list of decay times for each pin 
fall_times = [None]*9

# initialise 1ms wait period
wait_time = 0.001

while True:
    # indexing variable
    i = 0

    for pin in pins:
        # set up input channels and drive them high
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)

        # halt the program for 1ms to allow for capacitor charging
        time.sleep(wait_time)

        # measure the time for the capacitor to decay
        start_time = time.time()

        # initialise timeout condition
        timout = start_time + 0.01

        # set pin to an intput to begin measuring the discharge time
        GPIO.setup(pin, GPIO.IN)

        while GPIO.input(pin) and time.time() < timout:
            pass

        # find absolute time after pin has gone low
        end_time = time.time()

        # calculate discharge time
        discharge_time = end_time - start_time

        # add time to list
        fall_times[i] = discharge_time

        # increment index
        i += 1
    
    print(fall_times)

    # halt the program for 1 seconds
    time.sleep(1)
