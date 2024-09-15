import RPi.GPIO as GPIO
import time

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pins used for the 9 sensors
sensor_pins = [23, 20, 24, 16, 25, 12, 8, 1, 7]  # Example GPIO pins for 9 sensors

# Function to read sensor values and return as a binary array
def read_sensors():
    sensor_values = [0] * 9  # Initialize a 9-bit binary array
    for i in range(9):
        GPIO.setup(sensor_pins[i], GPIO.OUT)
        GPIO.output(sensor_pins[i], GPIO.LOW)
        time.sleep(0.00001)  # Small delay to discharge the capacitor
        
        # Set pin as input and wait for the sensor response
        GPIO.setup(sensor_pins[i], GPIO.IN)
        
        # Measure how long the pin stays high (sensor output)
        start_time = time.time()
        while GPIO.input(sensor_pins[i]) == GPIO.HIGH:
            pass
        elapsed_time = time.time() - start_time
        
        # Threshold value to detect a line (adjust based on sensor testing)
        threshold = 0.0005  # You may need to tweak this threshold value
        
        # If the elapsed time is below the threshold, it's detecting a line (black), otherwise white
        sensor_values[i] = 1 if elapsed_time < threshold else 0
    
    return sensor_values  # Return the binary sensor array

# Clean up GPIO after usage
def cleanup():
    GPIO.cleanup()
