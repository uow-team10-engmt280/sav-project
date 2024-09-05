import RPi.GPIO as GPIO
import time

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

        # State tracking
        self.state = "START"
        self.distance_sensor_triggered = 0  # To track how many times the distance sensor was triggered
        self.timeout_start = None
        self.timeout_duration = 5  # Timeout duration in seconds
        self.motor_speed_normal = 50  # Example speed value for normal movement
        self.motor_speed_turn = 25    # Example speed value for turning
        
        # Setup GPIO mode
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.distance_sensor_gpio, GPIO.IN)
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

    def read_line_sensor(self):
        # Simulate reading the line sensor; this would normally involve GPIO inputs
        pass

    def check_distance_sensor(self):
        if GPIO.input(self.distance_sensor_gpio):
            if self.line_sensor_timeout():  # Check if timeout has been respected
                self.distance_sensor_triggered += 1
                print(f"Object detected by distance sensor, count: {self.distance_sensor_triggered}")
                if self.distance_sensor_triggered == 1:
                    self.state = "OBJECT_DETECTED"
                elif self.distance_sensor_triggered == 2:
                    self.state = "DROPPING_OFF"
            self.reset_distance_sensor_timeout()

    def move(self, speed=None):
        if speed is None:
            speed = self.motor_speed_normal
        print(f"Moving forward at speed {speed}")
        GPIO.output(self.motor_a_direction_gpio, GPIO.HIGH)  # Example direction
        GPIO.output(self.motor_b_direction_gpio, GPIO.HIGH)  # Example direction
        # Adjust the PWM to control motor speed
        GPIO.output(self.motor_a_speed_gpio, speed)
        GPIO.output(self.motor_b_speed_gpio, speed)

    def turn_left(self):
        print("Turning left at reduced speed")
        GPIO.output(self.motor_a_direction_gpio, GPIO.LOW)  # Change direction
        GPIO.output(self.motor_b_direction_gpio, GPIO.HIGH)
        self.move(self.motor_speed_turn)

    def turn_right(self):
        print("Turning right at reduced speed")
        GPIO.output(self.motor_a_direction_gpio, GPIO.HIGH)
        GPIO.output(self.motor_b_direction_gpio, GPIO.LOW)  # Change direction
        self.move(self.motor_speed_turn)

    def stop(self):
        print("Stopping SAV")
        GPIO.output(self.motor_a_speed_gpio, 0)
        GPIO.output(self.motor_b_speed_gpio, 0)

    def rotate_arm(self, direction):
        if direction == "left":
            print("Rotating arm left")
            self.arm_pwm.ChangeDutyCycle(10)  # Example position for left rotation
        elif direction == "right":
            print("Rotating arm right")
            self.arm_pwm.ChangeDutyCycle(5)  # Example position for right rotation
        time.sleep(1)  # Simulate time taken to rotate the arm
        # Return arm to original position
        print("Returning arm to original position")
        self.arm_pwm.ChangeDutyCycle(7.5)
        time.sleep(1)

    def close_grip(self):
        print("Closing grip")
        self.grip_pwm.ChangeDutyCycle(12.5)  # Example position for closing grip
        time.sleep(1)  # Simulate time taken to close the grip

    def open_grip(self):
        print("Opening grip")
        self.grip_pwm.ChangeDutyCycle(7.5)  # Example position for opening grip
        time.sleep(1)  # Simulate time taken to open the grip

    def pickup_object(self):
        print("Picking up object")

        # Simulated machine vision input
        vision_input = "object_left"  # This would be determined by your vision system

        if vision_input == "object_left":
            self.rotate_arm("left")
        elif vision_input == "object_right":
            self.rotate_arm("right")

        self.close_grip()  # Close the grip to pick up the object
        print("Object picked up, arm returned to original position")

        # Return arm to original position
        self.rotate_arm("center")

    def dropoff_object(self):
        print("Dropping off object")

        # Simulated machine vision input
        vision_input = "drop_left"  # This would be determined by your vision system

        if vision_input == "drop_left":
            self.rotate_arm("left")
        elif vision_input == "drop_right":
            self.rotate_arm("right")

        self.open_grip()  # Open the grip to drop the object
        print("Object dropped off, arm returned to original position")

        # Return arm to original position
        self.rotate_arm("center")

    def line_sensor_timeout(self):
        if self.timeout_start is None:
            self.timeout_start = time.time()

        if time.time() - self.timeout_start > self.timeout_duration:
            self.timeout_start = None  # Reset timeout
            return True
        return False

    def reset_distance_sensor_timeout(self):
        print("Starting distance sensor timeout")
        self.timeout_start = time.time()

    def run(self):
        while True:
            self.read_line_sensor()
            self.check_distance_sensor()

            if self.state == "START":
                self.move()
                if GPIO.input(self.distance_sensor_gpio):
                    self.state = "OBJECT_DETECTED"
                elif self.line_sensor_data == self.parking_binary:
                    self.state = "PARKED"

            elif self.state == "TURN_LEFT":
                self.turn_left()
                if self.line_sensor_timeout():
                    self.state = "MOVING_AGAIN"

            elif self.state == "TURN_RIGHT":
                self.turn_right()
                if self.line_sensor_timeout():
                    self.state = "MOVING_AGAIN"

            elif self.state == "OBJECT_DETECTED":
                self.stop()
                self.pickup_object()
                self.reset_distance_sensor_timeout()
                self.state = "TIMEOUT"

            elif self.state == "DROPPING_OFF":
                self.stop()
                self.dropoff_object()
                self.reset_distance_sensor_timeout()
                self.state = "TIMEOUT"

            elif self.state == "TIMEOUT":
                self.move()  # Continue moving during the timeout
                if self.line_sensor_timeout():
                    self.state = "MOVING_AGAIN"

            elif self.state == "MOVING_AGAIN":
                self.move()
                if self.line_sensor_data == self.parking_binary:
                    self.state = "PARKED"
                elif GPIO.input(self.distance_sensor_gpio) and self.distance_sensor_triggered < 2:
                    self.state = "OBJECT_DETECTED"
                elif GPIO.input(self.distance_sensor_gpio) and self.distance_sensor_triggered == 2:
                    self.state = "DROPPING_OFF"

            elif self.state == "PARKED":
                self.stop()
                print("SAV is parked.")
                break  # Exit the loop once parked

            time.sleep(0.1)  # Small delay to prevent excessive CPU usage

if __name__ == "__main__":
    try:
        sav = SAV()
        sav.run()
    except KeyboardInterrupt:
        print("Cleanup")
        GPIO.cleanup()
