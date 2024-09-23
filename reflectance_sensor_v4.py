
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# list of pins corresponding to reflectance sensor output lines
pins = [11, 17, 9, 4, 10, 14, 22, 15, 27]

# list of thresholds to determine whether the sensor is "sensing" white or black
min_white_thresholds = [446, 333, 337, 323, 289, 312, 337, 337, 415]
max_white_thresholds = [469, 395, 390, 371, 339, 356, 383, 355, 489]

min_black_thresholds = [2904, 1955, 2128, 1791, 1578, 1812, 1943, 1840, 2278]
max_black_thresholds = [3004, 2092, 2223, 1868, 1783, 1856, 1996, 1948, 2407]

# initialise list of decay times for each pin 
fall_times = [None]*9

# intialise list of outputs depending on sensor readings (white=1,black=0)
outputs = [None]*9

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

        discharge_time *= 10e5
        discharge_time = round(discharge_time)

        # compare discharge time against corresponding threshold value
        if discharge_time <= 1000:
            output = 1
        elif discharge_time > 1000:
            output = 0
        else:
            output = '?'

        # add time to list
        fall_times[i] = discharge_time

        # add output to list
        outputs[i] = output

        # increment index
        i += 1
    
    #print(fall_times)
    #print("\n")
    print(outputs)

    # halt the program for 1 seconds
    time.sleep(1)
