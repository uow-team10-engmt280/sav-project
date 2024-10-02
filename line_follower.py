import time
import RPi.GPIO as GPIO
from MachineVisionLuca import *

class LineFollower:
    def __init__(self, pins, directions):
        # Ensure BCM mode is set for GPIO
        if GPIO.getmode() != GPIO.BCM:
            GPIO.setmode(GPIO.BCM)

        self.drive = Drive(motor_pins)  # Creating motor object
        self.pins = pins                # List of GPIO pins corresponding to reflectance sensor output lines
        self.directions = directions    # List of directions for the car to turn at forks
        self.check_flag = False

        global fork_counter
        global state
        global check_flag

        fork_counter = 0
        state = 'on line'

    def get_sensor_outputs(self):
        # Initialize list of decay times and sensor outputs
        fall_times = [None] * len(self.pins)
        outputs = [None] * len(self.pins)

        for i, pin in enumerate(self.pins):
            # Set up input channels and drive them high
            GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)

            # Allow the capacitors to charge
            time.sleep(0.001)

            # Measure the time for the capacitor to decay
            start_time = time.time()
            timeout = start_time + 0.01

            # Set pin to input to begin measuring discharge time
            GPIO.setup(pin, GPIO.IN)

            while GPIO.input(pin) and time.time() < timeout:
                pass

            end_time = time.time()

            # Calculate the discharge time in microseconds
            discharge_time = round((end_time - start_time) * 1e6)

            # Determine sensor output (1 = white, 0 = black)
            if discharge_time <= 800:
                outputs[i] = 1
            else:
                outputs[i] = 0

            # Store the discharge time (if needed)
            fall_times[i] = discharge_time

        # Clean up GPIO pins
        GPIO.cleanup(self.pins)

        return outputs

    def detect_fork(self, sensor_list):
        left_fork_sum = sum(sensor_list[:3])
        right_fork_sum = sum(sensor_list[-3:])
        line_sum = sum(sensor_list)

        # Fork detection logic
        if sensor_list[4] == 0 and left_fork_sum > 0 and right_fork_sum > 0:
            return True
        elif line_sum >= 5 and (sensor_list[0] == 0 or sensor_list[8] == 0):
            return True
        return False

    def determine_position(self, sensor_list, direction):
        # Check if car is derailed
        if sensor_list == [1] * 9:  
            # stop if on all white
            return self.drive.brake(100)    # Circuit complete - Stop motors
        if sensor_list == [0] * 9:
            # stop if on all black
            return self.drive.brake(100) # "Derailed - Motors stopped"

        if self.detect_fork(sensor_list):
            # Handling fork turning
            if direction:
                fork_list = [0, 0, 0, 0, 1, 1, 1, 1, 0]  # Right turn
            else:
                fork_list = [0, 1, 1, 1, 1, 0, 0, 0, 0]  # Left turn
        else:
            fork_list = sensor_list

        movement_patterns = {
            (0, 0, 0, 1, 1, 1, 0, 0, 0): self.drive.straight(70), #'Continue straight'
        }

        straying_left_patterns = {
            (0, 0, 0, 0, 1, 1, 1, 0, 0): self.drive.slight_rgt(),   # Straying left slightly
            (0, 0, 0, 1, 1, 1, 1, 0, 0): self.drive.slight_rgt(),   # Straying left slightly
            (0, 0, 0, 0, 0, 1, 1, 1, 0): self.drive.mild_rgt(),     # Straying left
            (0, 0, 0, 0, 1, 1, 1, 1, 0): self.drive.mild_rgt(),     # Straying left
            (0, 0, 0, 0, 0, 0, 1, 1, 1): self.drive.moderate_rgt(), # Straying left considerably
            (0, 0, 0, 0, 0, 1, 1, 1, 1): self.drive.moderate_rgt(), # Straying left considerably
            (0, 0, 0, 0, 0, 0, 0, 1, 1): self.drive.sharp_rgt(),    # Straying very far left
            (0, 0, 0, 0, 0, 0, 0, 0, 1): self.drive.full_rgt(),     # Almost off track left
        }

        straying_right_patterns = {
            (0, 0, 1, 1, 1, 0, 0, 0, 0): self.drive.slight_lft(),   # Straying right slightly
            (0, 0, 1, 1, 1, 1, 0, 0, 0): self.drive.slight_lft(),   # Straying right slightly
            (0, 1, 1, 1, 0, 0, 0, 0, 0): self.drive.mild_lft(),     # Straying right
            (0, 1, 1, 1, 1, 0, 0, 0, 0): self.drive.mild_lft(),     # Straying right
            (1, 1, 1, 0, 0, 0, 0, 0, 0): self.drive.moderate_lft(), # Straying right considerably
            (1, 1, 1, 1, 0, 0, 0, 0, 0): self.drive.moderate_lft(), # Straying right considerably
            (1, 1, 0, 0, 0, 0, 0, 0, 0): self.drive.sharp_lft(),    # Straying very far right
            (1, 0, 0, 0, 0, 0, 0, 0, 0): self.drive.full_lft(),     # Almost off track right
        }

        if tuple(fork_list) in movement_patterns:
            return movement_patterns[tuple(fork_list)]
        elif tuple(fork_list) in straying_left_patterns:
            return straying_left_patterns[tuple(fork_list)]
        elif tuple(fork_list) in straying_right_patterns:
            return straying_right_patterns[tuple(fork_list)]

        return self.drive.brake(100) # Unknown sensor pattern - Stop

    def handle_turns(self, sensor_list):
        while True:  # Infinite loop to simulate continuous checking
            match state:
                case "on line":
                    # if in the "on line" state and 
                    if self.detect_fork(sensor_list):
                        print("Entering 'at fork' state")
                        state = "at fork"
                        # if we are at the third junction, stop, check the directions from the camera tower
                        if fork_counter == 3:
                            self.drive.brake(100)
                            self.check_flag = True

                case "at fork":
                    if not self.detect_fork(sensor_list):
                        print("Exiting 'at fork' and entering 'on line' state")
                        state = "on line"
                        fork_counter += 1

class Drive:
    def __init__(self, motor_pins):
        self.motor_lft = Motor(motor_pins[:2], "LEFT")
        self.motor_rgt = Motor(motor_pins[2:], "RIGHT")

    def straight(self, speed):
        self.motor_lft.forward(speed)
        self.motor_rgt.forward(speed)

    def reverse(self, speed):
        self.motor_lft.reverse(speed)
        self.motor_rgt.reverse(speed)

    def brake(self, speed):
        self.motor_lft.brake(speed)
        self.motor_rgt.brake(speed)

    def slight_lft(self, speed):
        # Left: speed * 0.1, Right: speed
        self.motor_lft.reverse(0.1*speed)
        self.motor_rgt.forward(speed)

    def mild_lft(self, speed):
        # Left: speed * 0.25, Right: speed
        self.motor_lft.reverse(0.25*speed)
        self.motor_rgt.forward(speed)
    
    def moderate_lft(self, speed):
        # Left: speed * 0.4, Right: speed
        self.motor_lft.reverse(0.4*speed)
        self.motor_rgt.forward(speed)
    
    def sharp_lft(self, speed):
        # Left: speed * 0.5, Right: speed
        self.motor_lft.reverse(0.5*speed)
        self.motor_rgt.forward(speed)

    def full_lft(self, speed):
        # Left: speed * 0.8, Right: speed
        self.motor_lft.reverse(0.8*speed)
        self.motor_rgt.forward(speed)

    def slight_rgt(self, speed):
        # Left: speed, Right: speed * 0.1
        self.motor_rgt.reverse(0.1*speed)
        self.motor_lft.forward(speed)

    def mild_rgt(self, speed):
        # Left: speed, Right: speed * 0.25
        self.motor_rgt.reverse(0.25*speed)
        self.motor_lft.forward(speed)
    
    def moderate_rgt(self, speed):
        # Left: speed, Right: speed * 0.4
        self.motor_rgt.reverse(0.4*speed)
        self.motor_lft.forward(speed)
    
    def sharp_rgt(self, speed):
        # Left: speed, Right: speed * 0.5
        self.motor_rgt.reverse(0.5*speed)
        self.motor_lft.forward(speed)

    def full_rgt(self, speed):
        # Left: speed, Right: speed * 0.8
        self.motor_rgt.reverse(0.8*speed)
        self.motor_lft.forward(speed)

class Motor:
    def __init__(self, motor_pins: list[int], side: str, pwm_freq = 1000):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(motor_pins[0], GPIO.OUT)
        GPIO.setup(motor_pins[1], GPIO.OUT)


        self.motor_pins = motor_pins
        self.side = side

        # self.pwm_freq = pwm_freq

        self.pwm1 = GPIO.PWM(motor_pins[0], pwm_freq)
        self.pwm2 = GPIO.PWM(motor_pins[1], pwm_freq)

        self.pwm1.start(0)
        self.pwm2.start(0)

    def forward(self, speed):
        # IN1 = PWM: speed, IN2 = 0 => Forward
        self.pwm1.stop()
        self.pwm2.stop()
        
        self.pwm1.start(0)
        self.pwm2.start(0)
        
        GPIO.output(self.motor_pins[0], GPIO.HIGH)
        GPIO.output(self.motor_pins[1], GPIO.LOW)

        self.pwm1.ChangeDutyCycle(speed)
        self.pwm2.ChangeDutyCycle(0)

        print(f"{self.side} motor going FORWARD at a speed of {speed}")

    def reverse(self, speed):
        # IN1 = 0, IN2 = PWM: speed => Reverse
        self.pwm1.stop()
        self.pwm2.stop()
        
        self.pwm1.start(0)
        self.pwm2.start(0)
        
        GPIO.output(self.motor_pins[0], GPIO.LOW)
        GPIO.output(self.motor_pins[1], GPIO.HIGH)
        
        self.pwm1.ChangeDutyCycle(0)
        self.pwm2.ChangeDutyCycle(speed)

        print(f"{self.side} motor REVERSING at a speed of {speed}")

    def brake(self, speed):
        # IN1 = HIGH, IN2 = HIGH => Brake
        self.pwm1.stop()
        self.pwm2.stop()
        
        self.pwm1.start(0)
        self.pwm2.start(0)
        
        GPIO.output(self.motor_pins[0], GPIO.HIGH)
        GPIO.output(self.motor_pins[1], GPIO.HIGH)

        self.pwm1.ChangeDutyCycle(100 - speed)  # Use reverse braking (100 - PWM %)
        self.pwm2.ChangeDutyCycle(100 - speed)

        print(f"{self.side} motor BRAKING at a speed of {speed}")

    def coast(self):
        # IN1 = 0, IN2 = 0 => Coast
        self.pwm1.stop()
        self.pwm2.stop()

        self.pwm1.start(0)
        self.pwm2.start(0)

        GPIO.output(self.motor_pins[0], GPIO.LOW)
        GPIO.output(self.motor_pins[1], GPIO.LOW)

        print(f"{self.side} motor COASTING...")

    def cleanup(self):
        print(f"{self.side} motor GPIO cleanup.")

        self.pwm1.stop()
        self.pwm2.stop()
        
        GPIO.cleanup(self.motor_pins)

# example in main
pins = [11, 5, 9, 4, 10, 14, 22, 8, 16]  # reflectance sensor GPIO pins
motor_pins = [24, 23, 27, 17]   # motor gpio pins
mv_out = MV()   # get output from luca machine vision
directions = [mv_out[0]] * 2            # create directions list from mv output
line_follower = LineFollower(pins, directions)      # create line follower instance

while True:
    sensor_outputs = line_follower.get_sensor_outputs()     # get sensor outputs

    if line_follower.check_flag:        # if we are a third fork get new directions, update the directions list, reset the fork counter
        mv_out2 = MV()
        directions = [mv_out2[0]]*2
        fork_counter = 0
    
    line_follower.handle_turns(sensor_outputs, directions)  # check if we are at a fork, if we are at the third fork, stop and wait for updated directions
    position = line_follower.determine_position(sensor_outputs, directions[fork_counter])   # determines position based on current sensor outputs and current direction
