import RPi.GPIO as GPIO
import time

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pins used for the 9 sensors
sensor_pins = [23, 20, 24, 16, 25, 12, 8, 1, 7]  # Example GPIO pins for 9 sensors

# Initialize the binary array to store the sensor values
sensor_values = [0] * 9  # 9-bit binary array to hold sensor readings (1 or 0)

# Function to read sensor values
def read_sensors():
    global sensor_values
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
        
        # If the elapsed time is below the threshold, it's detecting a line (black), otherwise it's detecting white
        sensor_values[i] = 1 if elapsed_time < threshold else 0

# Main loop
try:
    while True:
        read_sensors()
        print(f'Sensor values: {sensor_values}')  # Print the binary array (1 for line, 0 for no line)
        time.sleep(0.1)  # Small delay before reading the sensors again

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()  # Clean up GPIO on exit
