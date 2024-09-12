# Author: Taro Bense
# ENGMT280 QTRX-HD-09RC interfacing module V2.4.6
# Changelog: add docstrings for the LineSensor class
# Still to fix: create calibration method to get threshold
# Date: 12/09/2024
# Time: 23:33:51
import time
import RPi.GPIO as GPIO


class LineSensor:
    '''
        A class that represents the Pololu QTRX-HD-09RC reflectance sensor.
        ref: https://www.pololu.com/product/4109
        ...
        Attributes
        ----------
        sensor_pins : list[int]
            the BCM numberinng of the pins connected to the line sensor
        max_value : float
            maximum possible discharge time of a single sensor
        threshold : float
            the value that seperates light and dark discharge times

        Methods
        -------
        emitters_off(wait=True):
            turns the IR LEDs off
        emitters_on(wait=True):
            turns the IR LEDs on
        read():
            main method used to read the line sensors outputted discharge times and 
            outputs the values to the user
        cleanup():
            cleans the GPIO pin allocations
    '''

    def __init__(self, ctrl_pin, sensor_pins, max_value, threshold=None):
        self.ctrl_pin = ctrl_pin  # control pin
        self.sensor_pins = sensor_pins  # array of gpio pins connected to sensor
        self._sensor_count = len(sensor_pins)  # amount of sensors
        # this is the maximum possible discharge time of the RC circuit
        self.max_value = max_value

        self._calibration_on = {'maximum': [0] * self._sensor_count, 'minimum': [
            self.max_value] * self._sensor_count, 'initialized': False}

        # create threshold to seperate light and dark values
        if threshold is None:
            # create value if not provided
            self.threshold = max_value / 2
        else:
            # use user input value
            self.threshold = threshold

        # set pin naming convention
        GPIO.setmode(GPIO.BCM)

        # set control pin (IR LED controller) to output
        GPIO.setup(ctrl_pin, GPIO.OUT)

        # set data pin I/O lines to outputs
        for pin in self.sensor_pins:
            GPIO.setup(pin, GPIO.OUT)

    def emitters_off(self, wait=True):
        if self.ctrl_pin:
            GPIO.output(self.ctrl_pin, GPIO.LOW)
        if wait:
            time.sleep(0.0012)

    def emitters_on(self, wait=True):
        if self.ctrl_pin:
            GPIO.output(self.ctrl_pin, GPIO.HIGH)
        if wait:
            time.sleep(0.0012)

    def read(self):
        while True:
            sensor_values = [self.max_value] * self._sensor_count
            read_flag = [False] * self._sensor_count

            # turn IR LEDs on
            # self.emitters_on()

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
                # elapsed_time = (time.time() - start_time) * 1000000
                elapsed_time = time.time() - start_time

                if elapsed_time > self.max_value:
                    break  # Stop if time exceeds the maximum threshold

                for i in range(self._sensor_count):
                    if not read_flag[i]:
                        if GPIO.input(self.sensor_pins[i]) == GPIO.LOW and elapsed_time < sensor_values[i]:
                            sensor_values[i] = elapsed_time
                            read_flag[i] = True

                if all(read_flag):
                    break
            # turn IR LEDs off
            # self.emitters_off()

            binary_array = [(0 if time_val > self.threshold else 1)
                            for time_val in sensor_values]

            return binary_array  # outputs discharge time in microsecs

    def calibrate(self):
        sensor_values = self.read()
        for i in range(self._sensor_count):
            self._calibration_on['maximum'][i] = max(
                self._calibration_on['maximum'][i], sensor_values[i])
            self._calibration_on['minimum'][i] = min(
                self._calibration_on['minimum'][i], sensor_values[i])

    def readCalibrated(self):
        sensor_values = self.read()
        for i in range(self._sensor_count):
            cal_min = self._calibration_on['minimum'][i]
            cal_max = self._calibration_on['maximum'][i]
            sensor_values[i] = (sensor_values[i] - cal_min) * \
                1000 // (cal_max - cal_min) if cal_max > cal_min else 0

        return sensor_values

    def cleanup(self):
        GPIO.cleanup()


# this runs if file is run as a program instead of used as a module/library
if __name__ == "__main__":
    # QTRX-HD-09RC values used for R, C and tau
    RESISTANCE = 500
    CAPACITANCE = 2.2E-9
    TIME_CONSTANT = RESISTANCE * CAPACITANCE
    max_discharge = 0.05

    # define control pin
    CTRL_PIN = 18
    # Example GPIO pins for the sensors
    sensor_pins = [23, 20, 24, 16, 25, 12, 8, 1, 7]

    sensors = LineSensor(CTRL_PIN, sensor_pins, max_discharge)

    while True:
        try:
            sensor_values = sensors.read()

            while True:
                print(sensor_values)
        finally:
            sensors.cleanup()
