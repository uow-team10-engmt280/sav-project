import RPi.GPIO as GPIO
import time
#from machine_vision import panel_directions  # Import the 2-bit array from machine_vision.py
import reflectance_sensor_v5 as ls

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
            if ls.get_sensor_outputs() == line_Sensor_forward:
                print("Go Forward\n")
            elif ls.get_sensor_outputs() == line_Sensor_left:
                print("Turn Left\n")
            elif ls.get_sensor_outputs() == line_Sensor_right:
                print("Turn Right\n")
            elif ls.get_sensor_outputs() == line_Sensor_slight_offtrack_left:
                print("Offtrack left\n")
            elif ls.get_sensor_outputs() == line_Sensor_slight_offtrack_right:
                print("Offtrack right\n")
            elif ls.get_sensor_outputs() == line_Sensor_offtrack:
                print("Offtrack\n")
            elif ls.get_sensor_outputs() == line_Sensor_left:
                print("Turn Left\n")
            elif ls.get_sensor_outputs() == line_Sensor_sharpleft:
                print("Sharp Left\n")
            elif ls.get_sensor_outputs() == line_Sensor_sharpright:
                print("Sharp Right")
            else:
                print("???\n")
            
            

if __name__ == "__main__":
    try:
        while True
            sav = SAV()
            sav.run()
    except KeyboardInterrupt:
        print("Cleanup")
        GPIO.cleanup()

