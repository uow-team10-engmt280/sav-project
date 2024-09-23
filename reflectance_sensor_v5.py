
import time
import RPi.GPIO as GPIO

def get_sensor_outputs():
    # check that pin numbering is set to BCM
    if GPIO.getmode() != GPIO.BCM:
        GPIO.setmode(GPIO.BCM)

    # list of pins corresponding to reflectance sensor output lines
    pins = [11, 17, 9, 4, 10, 14, 22, 15, 27]

    # initialise list of decay times for each pin 
    fall_times = [None]*9

    # intialise list of outputs depending on sensor readings (white=1,black=0)
    outputs = [None]*9

    # iterating variable
    i = 0

    for pin in pins:
        # set up input channels and drive them high
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)

        # halt the program for 1ms to allow for capacitor charging
        time.sleep(0.001)

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

        # calculate discharge time and convert to milliseconds and round for easier handling
        discharge_time = round((end_time - start_time)*1e6)      

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
    
    # print outputs
    print(outputs)

    # halt the program for 1 seconds
    time.sleep(1)

    # clean up pins used by the reflectance sensor
    GPIO.cleanup(pins)

    # return the list of sensor outputs
    return outputs
