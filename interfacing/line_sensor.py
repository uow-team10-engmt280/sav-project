# Author: Taro Bense
# ENGMT280 QTRX-HD-09RC interfacing module V2.3.2
# Changelog: fix some bugs in calibration method
# Still to fix: fix calibration methods, fix threshold ranging
import RPi.GPIO as GPIO
import time
from itertools import cycle

class lineSensor:
    def __init__(self, ctrl_pin, sensor_pins, max_value, threshold = None):
        self.ctrl_pin = ctrl_pin # control pin
        self.sensor_pins = sensor_pins # array of gpio pins connected to sensor
        self._sensor_count = len(sensor_pins) # amount of sensors
        # this is the maximum possible discharge time of the RC circuit
        self.max_value = max_value
        self._calibration_on = {'maximum': [], 'minimum': [], 'initialized': False}
        self._calibration_off = {'maximum': [], 'minimum': [], 'initialized': False}

        if threshold is None:
            self.threshold = max_value / 2
        else:
            self.threshold = threshold
        
        # set pin naming convention
        GPIO.setmode(GPIO.BCM)

        # set control pin (IR LED controller) to output
        GPIO.setup(ctrl_pin, GPIO.OUT)

        # set data pin I/O lines to outputs
        for pin in self.sensor_pins:
            GPIO.setup(pin, GPIO.OUT)
    
    def emitters_off(self, wait = True):
        if self.ctrl_pin:
            GPIO.output(self.ctrl_pin, GPIO.LOW)
        if wait:
            time.sleep(0.0012)

    def emitters_on(self, wait = True):
        if self.ctrl_pin:
            GPIO.output(self.ctrl_pin, GPIO.HIGH)
        if wait:
            time.sleep(0.0012)

    def read(self):
        sensor_values = [self.max_value] * self._sensor_count

        # turn IR LEDs on
        self.emittors_on()

        # drive data pins high
        for i in range(self._sensor_count):
            GPIO.output(self.sensor_pins[i], GPIO.HIGH)

        # wait for 10 microsecs
        time.sleep(0.00001)  # 10 microseconds

        # start timing
        start_time = time.time()

        # set data I/O lines to input
        for i in range(self._sensor_count):
            GPIO.setup(self.sensor_pins[i], GPIO.IN)

        # measure the discharge time
        while True:
            # convert to microseconds
            elapsed_time = (time.time() - start_time) * 1000000

            if elapsed_time > self.max_value:
                break  # Stop if time exceeds the maximum threshold

            for i in range(self._sensor_count):
                if GPIO.input(self.sensor_pins[i]) == GPIO.LOW and elapsed_time < sensor_values[i]:
                    sensor_values[i] = elapsed_time

        # turn IR LEDs off
        self.emitters_off()
        
        binary_array = [(0 if time > self.threshold else 1) for time in sensor_values]

        return binary_array # outputs discharge time in microsecs

    def calibrate(self):
        sensor_values = self.read()
        for i in range(self._sensor_count):
            self._calibration_on['maximum'][i] = max(self._calibration_on['maximum'][i], sensor_values[i])
            self._calibration_on['minimum'][i] = min(self._calibration_on['minimum'][i], sensor_values[i])

    def readCalibrated(self):
        sensor_values = self.read()
        for i in range(self._sensor_count):
            cal_min = self._calibration_on['minimum'][i]
            cal_max = self._calibration_on['maximum'][i]
            sensor_values[i] = (sensor_values[i] - cal_min) * 1000 // (cal_max - cal_min) if cal_max > cal_min else 0

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
            cycle_values = cycle(sensor_values)
            
            while True:
                print(next(cycle_values))
        finally:
            sensors.cleanup()