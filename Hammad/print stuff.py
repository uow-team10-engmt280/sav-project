import RPi.GPIO as GPIO
import time
from machine_vision import panel_directions  # Import the 2-bit array from machine_vision.py
from line_sensor import binary_array

class SAV:
    def __init__(self):
        global line_Sensor_forward = [0,0,0,1,1,1,0,0,0]
        global line_Sensor_left = [1,1,1,0,0,0,0,0,0]
        global line_Sensor_right = [0,0,0,0,0,0,1,1,1]
        global line_Sensor_slight_offtrack_left = [0,1,1,1,0,0,0,0,0]
        global line_Sensor_slight_offtrack_right = [0,0,0,0,0,1,1,1,0]
        global line_Sensor_offtrack = [0,0,0,0,0,0,0,0,0]
        global line_Sensor_sharpleft = [1,1,0,0,0,0,0,0,0]
        global line_Sensor_sharpright = [0,0,0,0,0,0,0,1,1]
      
    def run(self):
        while True:
          if 

if __name__ == "__main__":
    try:
        sav = SAV()
        sav.run()
    except KeyboardInterrupt:
        print("Cleanup")
        GPIO.cleanup()

