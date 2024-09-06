#import RPi.GPIO as GPIO
import time
import line_sensor as ls

class SAV:
    def __init__(self):
        global line_Sensor_forward
        line_Sensor_forward = [0,0,0,1,1,1,0,0,0]
        global line_Sensor_left
        line_Sensor_left = [1,1,1,0,0,0,0,0,0]
        global line_Sensor_right
        line_Sensor_right = [0,0,0,0,0,0,1,1,1]
        global line_Sensor_slight_offtrack_left
        line_Sensor_slight_offtrack_left = [0,1,1,1,0,0,0,0,0]
        global line_Sensor_slight_offtrack_right
        line_Sensor_slight_offtrack_right = [0,0,0,0,0,1,1,1,0]
        global line_Sensor_offtrack
        line_Sensor_offtrack = [0,0,0,0,0,0,0,0,0]
        global line_Sensor_sharpleft
        line_Sensor_sharpleft = [1,1,0,0,0,0,0,0,0]
        global line_Sensor_sharpright
        line_Sensor_sharpright = [0,0,0,0,0,0,0,1,1]
      
    def run(self):
        while True:
            if ls.read() == line_Sensor_forward:
                print("Go Forward")
            elif ls.read() == line_Sensor_left:
                print("Turn Left")
            elif ls.read() == line_Sensor_right:
                print("Turn Right")
            elif ls.read() == line_Sensor_slight_offtrack_left:
                print("Offtrack left")
            elif ls.read() == line_Sensor_slight_offtrack_right:
                print("Offtrack right")
            elif ls.read() == line_Sensor_offtrack:
                print("Offtrack")
            elif ls.read() == line_Sensor_left:
                print("Turn Left")
            elif ls.read() == line_Sensor_sharpleft:
                print("Sharp Left")
            elif ls.read() == line_Sensor_sharpright:
                print("Sharp Right")
            
            

if __name__ == "__main__":
        # QTRX-HD-09RC values used for R, C and tau
    RESISTANCE = 220
    CAPACITANCE = 2.2E-9
    TIME_CONSTANT = RESISTANCE * CAPACITANCE
    max_discharge = 6 * TIME_CONSTANT

    # define control pin
    CTRL_PIN = 18
    # Example GPIO pins for the sensors
    sensor_pins = [23, 20, 24, 16, 25, 12, 8, 1, 7]
    sensors = ls.lineSensor(CTRL_PIN, sensor_pins, max_discharge)
    try:
        sav = SAV()
        sav.run()
    except KeyboardInterrupt:
        print("Cleanup")
        GPIO.cleanup()

