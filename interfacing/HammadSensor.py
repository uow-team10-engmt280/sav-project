import RPi.GPIO as GPIO
import time

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pins used for the 9 sensors
sensor_pins = [23, 20, 24, 16, 25, 12, 8, 1, 7]  # Example GPIO pins for 9 sensors

# Function to read sensor values and return as a binary array
def read_sensors():
    sensor_values = [0,0,0,0,0,0,0,0,0]  # Initialize a 9-bit binary array
    for i in range(9):
        # Configure pin as output to discharge any charge
        GPIO.setup(sensor_pins[i], GPIO.OUT)
        GPIO.output(sensor_pins[i], GPIO.LOW)
        time.sleep(0.00001)  # Brief delay to ensure discharge
        
        # Set pin as input and wait for sensor response
        GPIO.setup(sensor_pins[i], GPIO.IN)
        
        # Measure the time the sensor pin stays high (indicating detection)
        start_time = time.time()
        while GPIO.input(sensor_pins[i]) == GPIO.HIGH:
            pass
        elapsed_time = time.time() - start_time
        
        # Threshold to differentiate between detecting black (line) and white (no line)
        threshold = 0.0005  # Adjust this based on sensor calibration
        
        # Store binary result based on detection time
        sensor_values[i] = 1 if elapsed_time < threshold else 0
    
    return sensor_values  # Return the binary array of sensor readings

# Clean up GPIO setup
def cleanup():
    GPIO.cleanup()  # Reset GPIO settings after use
