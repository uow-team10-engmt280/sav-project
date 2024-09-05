import RPi.GPIO as GPIO
import time

# Setup
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
GPIO_PIN = 12           # GPIO pin 12
GPIO.setup(GPIO_PIN, GPIO.OUT)

# Step 1: Set GPIO12 to OUT mode
GPIO.output(GPIO_PIN, GPIO.HIGH)

# Step 2: Wait for 10 microseconds
time.sleep(0.00001)  # 10 microseconds = 10 * 10^-6 seconds

# Step 3: Set GPIO12 to LOW
GPIO.output(GPIO_PIN, GPIO.LOW)

# Step 4: Start timer before setting GPIO12 to IN mode
start_time = time.time()

# Step 5: Set GPIO12 to IN mode
GPIO.setup(GPIO_PIN, GPIO.IN)

# Step 6: Measure the time for the pin to go LOW
while GPIO.input(GPIO_PIN) == GPIO.HIGH:
    pass

end_time = time.time()

# Calculate the duration
duration = end_time - start_time
print(f"Time for GPIO12 to go LOW: {duration:.10f} seconds")

# Cleanup
GPIO.cleanup()
