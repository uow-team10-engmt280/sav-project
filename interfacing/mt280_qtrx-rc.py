# Author: Taro Bense
# ENGMT280 QTRX-HD-09RC interfacing module V1.2.0
# Changelog: modularised code; improved timing method; finalised output method
import RPi.GPIO as GPIO
import time

class lineSensor:
    def __init__(self, ctrl_pin, sensor_pins, max_value):
        self.ctrl_pin = ctrl_pin # control pin
        self.sensor_pins = sensor_pins # array of gpio pins connected to sensor
        self.sensor_count = len(sensor_pins) # amount of sensors
        # this is the maximum possible discharge time of the RC circuit
        self.max_value = max_value
        
        # set pin naming convention
        GPIO.setmode(GPIO.BCM)

        # set control pin (IR LED controller) to output
        GPIO.setup(ctrl_pin, GPIO.OUT)

        # set data pin I/O lines to outputs
        for pin in self.sensor_pins:
            GPIO.setup(pin, GPIO.OUT)

    def read(self):
        sensor_values = [self.max_value] * self.sensor_count

        # turn IR LEDs on
        GPIO.output(CTRL_PIN, GPIO.HIGH)

        # drive data pins high
        for i in range(self.sensor_count):
            GPIO.output(self.sensor_pins[i], GPIO.HIGH)

        # wait for 10 microsecs
        time.sleep(0.00001)  # 10 microseconds

        # start timing
        start_time = time.time()

        # set data I/O lines to input
        for i in range(self.sensor_count):
            GPIO.setup(self.sensor_pins[i], GPIO.IN)

        # measure the discharge time
        while True:
            # convert to microseconds
            elapsed_time = (time.time() - start_time) * 1000000

            if elapsed_time > self.max_value:
                break  # Stop if time exceeds the maximum threshold

            for i in range(self.sensor_count):
                if GPIO.input(self.sensor_pins[i]) == GPIO.LOW and elapsed_time < sensor_values[i]:
                    sensor_values[i] = elapsed_time

        # turn IR LEDs off
        GPIO.output(CTRL_PIN, GPIO.LOW)

        return sensor_values
    
    def cleanup(self):
        GPIO.cleanup()

# this runs if python program is run instead of used as a module
if __name__ == "__main__":
    RESISTANCE = 220
    CAPACITANCE = 2.2E-9
    TIME_CONSTANT = RESISTANCE * CAPACITANCE
    max_discharge = 6 * TIME_CONSTANT

    # define control pin
    CTRL_PIN = 18
    # Example GPIO pins for the sensors
    sensor_pins = [23, 20, 24, 16, 25, 12, 8, 1, 7]
    
    sensors = lineSensor(CTRL_PIN, sensor_pins, max_discharge)
    
    while True:
        try:
            sensor_values = sensors.read()
            print(sensor_values)
        finally:
            sensors.cleanup()