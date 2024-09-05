import RPi.GPIO as GPIO
import time
import numpy as np  # Import NumPy for array handling

class ReflectanceSensorArray:
    def __init__(self, sensor_pins, control_pins):
        self.sensor_pins = sensor_pins
        self.control_pins = control_pins

        # Setup GPIO mode
        GPIO.setmode(GPIO.BCM)

        # Set up the sensor pins as inputs
        for pin in self.sensor_pins:
            GPIO.setup(pin, GPIO.IN)

        # Set up the control pins as outputs
        for pin in self.control_pins.values():
            GPIO.setup(pin, GPIO.OUT)

    def read_sensors(self):
        """Reads the current state of the sensors and returns as a NumPy array."""
        return np.array([GPIO.input(pin) for pin in self.sensor_pins])

    def perform_gpio_operation(self):
        """Performs a GPIO operation based on sensor readings."""
        even_control_pin = self.control_pins["EVEN_control"]
        GPIO.setup(even_control_pin, GPIO.OUT)
        GPIO.output(even_control_pin, GPIO.HIGH)
        time.sleep(0.00001)  # Wait for 10 microseconds
        GPIO.output(even_control_pin, GPIO.LOW)
        GPIO.setup(even_control_pin, GPIO.IN)

        # Measure the time for a sensor to change state (example: Sensor 6)
        start_time = time.time()
        while GPIO.input(self.sensor_pins[5]) == GPIO.HIGH:  # Using Sensor 6 arbitrarily
            pass
        duration = time.time() - start_time

        print(f"Time for Sensor 6 to go LOW: {duration:.10f} seconds")

    def cleanup(self):
        """Cleans up the GPIO pins."""
        GPIO.cleanup()

def main():
    # GPIO Pin setup for sensors and control pins
    sensor_pins = [23, 20, 24, 16, 25, 12, 8, 7, 1]  # Sensor 1 through Sensor 9
    control_pins = {"ODD_control": 18, "EVEN_control": 21}

    sensor_array = ReflectanceSensorArray(sensor_pins, control_pins)

    try:
        while True:
            # Read sensor values and output them
            sensor_values = sensor_array.read_sensors()
            print(sensor_values)  # This can be sent to another program instead of just printing
            
            # Example of using the perform_gpio_operation if needed
            sensor_array.perform_gpio_operation()
            
            time.sleep(0.1)  # Small delay to avoid overloading the CPU
            
    except KeyboardInterrupt:
        print("Exiting...")
        
    finally:
        sensor_array.cleanup()

if __name__ == "__main__":
    main()
