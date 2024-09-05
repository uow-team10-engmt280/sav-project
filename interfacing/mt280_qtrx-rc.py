# Author: Taro Bense
# ENGMT280 QTRX-HD-09RC interfacing module V0.2.1
import RPi.GPIO as GPIO
import time 

# set pin naming convention
GPIO.setmode(GPIO.BCM)

# define all data and control pins
# v0.2.1 correct pin numbering
CTRL = 18
D_1 = 23
D_2 = 20
D_3 = 24
D_4 = 16
D_5 = 25
D_6 = 12
D_7 = 8
D_8 = 1
D_9 = 7

data_array = [2, 3, 4, 5, 6, 7, 8, 9, 10]
timing_arr = []
output_arr = []

# turn on IR LEDs
GPIO.setup(CTRL, GPIO.OUT)
GPIO.output(CTRL, GPIO.HIGH)

# make data pins output line
GPIO.setup(data_array, GPIO.OUT)

# set pins to high
GPIO.output(data_array, GPIO.HIGH)

# wait 10 microsecs
time.sleep(0.00001)

# set the data pins to inputs
GPIO.setup(data_array, GPIO.IN)

for d_pin in data_array:
    # start the timing
    timing_arr.append(time.time())
    # read the values and send to output_arr
    output_arr[d_pin] = GPIO.input(data_array[d_pin])
     
    while GPIO.input(data_array) == GPIO.HIGH:
        pass
    
    end_time = time.time()

# turn IR LEDs off
GPIO.output(CTRL, GPIO.LOW)

# calculate each dischrge time
for duration in timing_arr:
    timing_arr[duration] = end_time - timing_arr[duration]

# output each duration for debugging
for i in range(len(timing_arr) - 1):
    print(f"Time for data to go low: {timing_arr[i]:.10f} seconds.")

# cleanup gpio pins after use
GPIO.cleanup()
