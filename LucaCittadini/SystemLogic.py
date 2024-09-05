import RPi.GPIO as GPIO
import time
import gpio_timing  # Import the gpio_timing module

class SAVStateMachine:
    def __init__(self, move_pin, sensor_pin, side_sensor_pin):
        self.move_pin = move_pin
        self.sensor_pin = sensor_pin
        self.side_sensor_pin = side_sensor_pin
        self.state = 'STOP'
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.move_pin, GPIO.OUT)
        GPIO.setup(self.sensor_pin, GPIO.IN)
        GPIO.setup(self.side_sensor_pin, GPIO.IN)
        
    def move(self):
        print("Moving forward...")
        GPIO.output(self.move_pin, GPIO.HIGH)
        while GPIO.input(self.sensor_pin) == GPIO.HIGH:
            time.sleep(0.1)
        self.state = 'STOP'
        self.stop()
    
    def stop(self):
        print("Stopping...")
        GPIO.output(self.move_pin, GPIO.LOW)
        self.state = 'PICKUP'
        self.pickup_object()
        
    def pickup_object(self):
        print("Checking for object...")
        if GPIO.input(self.side_sensor_pin) == GPIO.HIGH:
            print("Object detected! Picking up object...")
            # Insert object pickup logic here
            time.sleep(2)
            self.state = 'TURN'
            self.turn()
        else:
            print("No object detected. Moving forward...")
            self.state = 'MOVE'
            self.move()
    
    def turn(self):
        print("Turning...")
        # Example: Measuring time for GPIO to go LOW using the gpio_timing module
        duration = gpio_timing.measure_gpio_low_duration(self.move_pin)
        print(f"Turn duration: {duration:.10f} seconds")
        # Insert turn logic here
        time.sleep(1)
        self.state = 'PARK'
        self.park()
    
    def park(self):
        print("Parking...")
        # Insert park logic here
        time.sleep(2)
        self.state = 'STOP'
        self.reset()
    
    def reset(self):
        print("Resetting...")
        GPIO.cleanup()
        self.state = 'STOP'
        print("Reset complete. System is stopped.")
    
    def run(self):
        while True:
            if self.state == 'MOVE':
                self.move()
            elif self.state == 'STOP':
                self.stop()
            elif self.state == 'PICKUP':
                self.pickup_object()
            elif self.state == 'TURN':
                self.turn()
            elif self.state == 'PARK':
                self.park()
            elif self.state == 'RESET':
                self.reset()
            else:
                print("Unknown state! Resetting...")
                self.reset()
                break

# Setup
move_pin = 12          # GPIO pin to control movement
sensor_pin = 18        # GPIO pin for line following sensor
side_sensor_pin = 23   # GPIO pin for object detection sensor

# Initialize the state machine
sav = SAVStateMachine(move_pin, sensor_pin, side_sensor_pin)

# Start the state machine
sav.state = 'MOVE'
sav.run()

