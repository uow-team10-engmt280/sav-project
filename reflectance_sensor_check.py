
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# list of pins corresponding to reflectance sensor output lines
pins = [11, 9, 10, 22, 27, 17, 4, 3, 2]

# initialise list of decay times for each pin 
fall_times = [None]*9

# indexing variable
i = 0

# initialise 1ms wait period
wait_time = 0.001

while True:
    for pin in pins:
        # set up input channels and drive them high
        GPIO.setup(pin, GPIO.IN, initial=GPIO.HIGH)

        # halt the program for 1ms to allow for capacitor charging
        time.sleep(wait_time)

        # measure the time for the capacitor to decay
        start_time = time.time()

        # set pin to an output to begin measuring the discharge time
        GPIO.setup(pin, GPIO.IN)

        while GPIO.input(pin):
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

    # halt the program for 1.5 seconds
    time.sleep(1.5)
