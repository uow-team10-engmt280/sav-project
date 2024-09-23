
import time
import RPi.GPIO as GPIO

# use BCM channel names
GPIO.setmode(GPIO.BCM)

# list of pins corresponding to reflectance sensor output lines
pins = [11, 9, 10, 22, 27, 17, 4, 3, 2]

# controls (14 controls odd, 15 even)
controls = [14, 15]

# initialise list of decay times for each pin 
fall_times = [None]*9

# initialise 1ms wait period
wait_time = 0.001

while True:
    # I was getting an error without this line, it said I needed to configure the board number scheme
    GPIO.setmode(GPIO.BCM)

    # indexing variable
    i = 0

    for pin in pins:
        # set up input channels and drive them high
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)

        # halt the program for 1ms to allow for capacitor charging
        time.sleep(wait_time)
        
        # without the flag and without the second counter variable the program would get stuck in the while loop
        flag = True
        j = pins.index(pin)     # substitute for "i"

        # measure the time for the capacitor to decay
        start_time = time.time()

        # set pin to an output to begin measuring the discharge time
        GPIO.setup(pin, GPIO.IN)

        while GPIO.input(pin) and flag:
            if pin == 3:
                j += 1      # this is where the program was getting stuck
            if j >= 8:
                j = 0
                flag = False    # only way to exit the while loop as far as I can tell
            pass

        # find absolute time after pin has gone low
        end_time = time.time()

        # calculate discharge time
        discharge_time = end_time - start_time

        # add time to list
        fall_times[i] = discharge_time

        # increment index
        i += 1
    
    # display sensor outputs
    print(fall_times)

    # halt the program for 1.5 seconds
    time.sleep(1.5)