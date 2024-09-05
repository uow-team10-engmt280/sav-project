import RPi.GPIO as GPIO
import time
from machine_vision import panel_directions  # Import the 2-bit array from machine_vision.py
from line_sensor import binary_array

class SAV:
    def __init__(self):
        # GPIO setup based on your provided mappings
        self.distance_sensor_gpio = 2  # Output of range sensor
        self.arm_servo_gpio = 0        # Servo Control
        self.grip_servo_gpio = 5       # Mini Servo Control
        self.motor_a_direction_gpio = 6 # Motor A direction control
        self.motor_a_speed_gpio = 13    # Motor A speed control
        self.motor_b_direction_gpio = 19 # Motor B direction control
        self.motor_b_speed_gpio = 26     # Motor B speed control
        self.line_sensor_gpio = 3        # Line sensor GPIO

        # State tracking
        self.state = "START"
        self.distance_sensor_triggered = 0
        self.timeout_start = None
        self.timeout_duration = 5  # Timeout duration in seconds
        self.motor_speed_normal = 50  # Example speed value for normal movement
        self.motor_speed_turn = 25    # Example speed value for turning
        
        # Setup GPIO mode
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.distance_sensor_gpio, GPIO.IN)
        GPIO.setup(self.line_sensor_gpio, GPIO.IN)  # Setup line sensor
        GPIO.setup(self.arm_servo_gpio, GPIO.OUT)
        GPIO.setup(self.grip_servo_gpio, GPIO.OUT)
        GPIO.setup(self.motor_a_direction_gpio, GPIO.OUT)
        GPIO.setup(self.motor_a_speed_gpio, GPIO.OUT)
        GPIO.setup(self.motor_b_direction_gpio, GPIO.OUT)
        GPIO.setup(self.motor_b_speed_gpio, GPIO.OUT)
        
        # Initialize PWM for servos
        self.arm_pwm = GPIO.PWM(self.arm_servo_gpio, 50)  # 50 Hz frequency
        self.grip_pwm = GPIO.PWM(self.grip_servo_gpio, 50)
        self.arm_pwm.start(7.5)  # Neutral position for arm (90 degrees)
        self.grip_pwm.start(7.5) # Neutral position for grip (open)

        # Use the imported panel directions
        self.panel_directions = panel_directions

        # Predefine pickup and dropoff directions and lanes
        self.pickup_direction = self.panel_directions[0][1]  # Direction for pickup (R/L)
        self.pickup_lane = self.panel_directions[0][0]       # Lane for pickup (R/L)
        
        self.dropoff_direction = self.panel_directions[1][1]  # Direction for dropoff (R/L)
        self.dropoff_lane = self.panel_directions[1][0]       # Lane for dropoff (R/L)

        global line_Sensor_forward = [0,0,0,1,1,1,0,0,0]
        global line_Sensor_left = [1,1,1,0,0,0,0,0,0]
        global line_Sensor_right = [0,0,0,0,0,0,1,1,1]
        global line_Sensor_slight_offtrack_left = [0,1,1,1,0,0,0,0,0]
        global line_Sensor_slight_offtrack_right = [0,0,0,0,0,1,1,1,0]
        global line_Sensor_offtrack = [0,0,0,0,0,0,0,0,0]
        global line_Sensor_sharpleft = [1,1,0,0,0,0,0,0,0]
        global line_Sensor_sharpright = [0,0,0,0,0,0,0,1,1]

    def move(self, speed=None):
        if speed is None:
            speed = self.motor_speed_normal
        print(f"Moving at speed {speed}")
        GPIO.output(self.motor_a_direction_gpio, GPIO.HIGH)  # Move forward
        GPIO.output(self.motor_b_direction_gpio, GPIO.HIGH)
        GPIO.output(self.motor_a_speed_gpio, speed)
        GPIO.output(self.motor_b_speed_gpio, speed)

    def stop(self):
        print("Stopping SAV")
        GPIO.output(self.motor_a_speed_gpio, 0)
        GPIO.output(self.motor_b_speed_gpio, 0)

    def turn(self, left=True):
        if left:
            print("Turning left")
            GPIO.output(self.motor_a_direction_gpio, GPIO.LOW)
            GPIO.output(self.motor_b_direction_gpio, GPIO.HIGH)
        else:
            print("Turning right")
            GPIO.output(self.motor_a_direction_gpio, GPIO.HIGH)
            GPIO.output(self.motor_b_direction_gpio, GPIO.LOW)
        self.move(self.motor_speed_turn)
        time.sleep(1)  # Duration for turning, adjust as needed

    def rotate_arm(self, direction):
        if direction == "L":
            # Adjust PWM for left rotation (example values)
            self.arm_pwm.ChangeDutyCycle(10)
        elif direction == "R":
            # Adjust PWM for right rotation (example values)
            self.arm_pwm.ChangeDutyCycle(5)
        time.sleep(1)  # Adjust as needed for arm rotation

    def handle_object(self, action):
        if action == "pickup":
            print(f"Picking up object from {self.pickup_lane} lane, {self.pickup_direction} direction")
            self.rotate_arm(self.pickup_lane)  # Rotate arm in the direction of the pickup lane
            self.grip_pwm.ChangeDutyCycle(12.5)  # Close grip
            time.sleep(1)
        elif action == "dropoff":
            print(f"Dropping off object in {self.dropoff_lane} lane, {self.dropoff_direction} direction")
            self.rotate_arm(self.dropoff_lane)  # Rotate arm in the direction of the dropoff lane
            self.grip_pwm.ChangeDutyCycle(7.5)  # Open grip
            time.sleep(1)

        self.arm_pwm.ChangeDutyCycle(7.5)  # Return arm to neutral

    def start_timeout(self):
        self.timeout_start = time.time()
        self.state = "TIMEOUT"

    def check_timeout(self):
        if self.timeout_start is not None and (time.time() - self.timeout_start) > self.timeout_duration:
            self.timeout_start = None  # Reset timeout
            self.state = "MOVING_AGAIN"

    def detect_fork(self):
        # Detect if the line sensor reads a fork (loss of central line)
        # This is a simplified logic assuming the sensor detects the split
        return GPIO.input(self.line_sensor_gpio) == 0  # Example condition

    def run(self):
        while True:
            if self.detect_fork():
                print("Fork detected")
                if self.pickup_lane == "L":
                    self.turn(left=True)
                else:
                    self.turn(left=False)
                self.state = "MOVING_AGAIN"

            if self.state != "TIMEOUT" and GPIO.input(self.distance_sensor_gpio):
                self.distance_sensor_triggered += 1
                if self.distance_sensor_triggered == 1:
                    self.stop()
                    self.handle_object("pickup")
                    self.start_timeout()  # Start timeout after pickup
                elif self.distance_sensor_triggered == 2:
                    self.stop()
                    self.handle_object("dropoff")
                    self.start_timeout()  # Start timeout after dropoff

            if self.state == "START":
                self.move()

            elif self.state == "TURN_LEFT":
                self.turn(left=True)
                self.state = "MOVING_AGAIN"

            elif self.state == "TURN_RIGHT":
                self.turn(left=False)
                self.state = "MOVING_AGAIN"

            elif self.state == "MOVING_AGAIN":
                self.move()

            elif self.state == "TIMEOUT":
                self move()  # Continue moving during the timeout
                self.check_timeout()

            time.sleep(0.1)  # Small delay to prevent excessive CPU usage

if __name__ == "__main__":
    try:
        sav = SAV()
        sav.run()
    except KeyboardInterrupt:
        print("Cleanup")
        GPIO.cleanup()
