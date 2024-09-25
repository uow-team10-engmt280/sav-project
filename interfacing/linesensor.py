# Author: Taro Bense
# ENGMT280 QTRX-HD-09RC interfacing module V2.5.0
# Changelog: refactor calibrate() method; add docstrings for LineSensor class methods
# Still to fix: create testing programs
# Date -> 13/09/2024
# Time -> 00:17
import time
import RPi.GPIO as GPIO


class LineSensor:
    """
        A class that represents the Pololu QTRX-HD-09RC reflectance sensor.
        ref: https://www.pololu.com/product/4109
        ...
        Attributes
        ----------
        sensor_pins : list[int]
            the BCM numbering of the pins connected to the line sensor.
        max_value : float
            maximum possible discharge time of a single sensor.
        threshold : float
            the value that seperates light and dark discharge times.

        Methods
        -------
        emitters_off(wait=True):
            turns the IR LEDs off.
        emitters_on(wait=True):
            turns the IR LEDs on.
        read():
            main method used to read the line sensors outputted discharge times and 
            outputs the values to the user.
        cleanup():
            cleans the GPIO pin allocations.
    """

    def __init__(self, ctrl_pin, sensor_pins, max_value, threshold=None):
        self.ctrl_pin = ctrl_pin  # control pin
        self.sensor_pins = sensor_pins  # array of gpio pins connected to sensor
        self._sensor_count = len(sensor_pins)  # amount of sensors
        # this is the maximum possible discharge time of the RC circuit
        self.max_value = max_value
        self._calibration_on = {'maximum': [0] * self._sensor_count, 'minimum': [
            self.max_value] * self._sensor_count, 'initialized': False}

        # create threshold to seperate light and dark values
        self.threshold = threshold if threshold is not None else max_value / 2

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
        """
            Reads the discharge times of the sensor and outputs the processed value 
            in single-digit binary values where light => 0 and dark => 1.
            ...
            Parameters
            ----------
            None

            Returns
            -------
            binary_array : list[int]
                a list of single-digit binary numbers representing the reflectance 
                levels sensed, it is returned with the same length as the amount of
                sensor pins used.
        """
        while True:
            sensor_values = [self.max_value] * self._sensor_count
            read_flag = [False] * self._sensor_count

            # turn IR LEDs on
            # self.emitters_on()

            # drive data pins high
            for pin in range(self._sensor_count):
                GPIO.output(self.sensor_pins[pin], GPIO.HIGH)

                # wait for 10 microsecs
                time.sleep(0.001)  # 10 microseconds

                # start timing
                start_time = time.time()

                # set data I/O lines to input
                GPIO.setup(self.sensor_pins[pin], GPIO.IN)

                while GPIO.input(sensor_values[pin]):
                    pass

                # measure the discharge time
                # convert to microseconds
                # elapsed_time = (time.time() - start_time) * 1000000
                elapsed_time = time.time() - start_time

                elapsed_time = round(elapsed_time * 10e6)

                # compare discharge time against corresponding threshold value
                if elapsed_time <= 1000:
                    output = 1
                elif elapsed_time > 1000:
                    output = 0
                else:
                    output = '?'

                sensor_values[sensor_pins.index(pin)] = output
                
            # turn IR LEDs off
            # self.emitters_off()

            # sensor_values = [(0 if time_val < self.threshold else 1) for time_val in sensor_values]

            return sensor_values  # outputs discharge time in microsecs

    def calibrate(self, num_samples=10):
        for _ in range(num_samples):
            sensor_values = self.read()

            for i in range(self._sensor_count):
                if sensor_values[i] > self._calibration_on['maximum'][i]:
                    self._calibration_on['maximum'][i] = sensor_values[i]

                if sensor_values[i] < self._calibration_on['minimum'][i]:
                    self._calibration_on['minimum'][i] = sensor_values[i]

    def readCalibrated(self):
        """
        Reads the sensor values and scales them based on the previously 
        recorded calibration data (maximum and minimum discharge times).

        Returns
        -------
        calibrated_values : list[int]
            A list of calibrated sensor values, scaled from 0 (minimum) to 
            1000 (maximum).
        """
        if not self._calibration_on['initialized']:
            raise ValueError(
                "Calibration has not been completed, run LineSensor.calibrate().")

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
    sensor_pins = [11, 17, 9, 4, 10, 14, 22, 15, 27]

    sensors = LineSensor(CTRL_PIN, sensor_pins, max_discharge)

    while True:
        try:
            sensor_values = sensors.read()

            while True:
                print(sensor_values)
        finally:
            sensors.cleanup()
