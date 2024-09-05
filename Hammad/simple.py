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
        self.distance_sensor_triggered = 0
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

        print("Straightening out")
        GPIO.output(self.motor_a_direction_gpio, not left)  # Opposite direction
        GPIO.output(self.motor_b_direction_gpio, left)
        self.move(self.motor_speed_turn)
        time.sleep(1)  # Duration for straightening out, adjust as needed

    def handle_object(self, action):
        if action == "pickup":
            print("Picking up object")
            self.arm_pwm.ChangeDutyCycle(5)  # Rotate arm to position
            time.sleep(1)
            self.grip_pwm.ChangeDutyCycle(12.5)  # Close grip
            time.sleep(1)
            self.arm_pwm.ChangeDutyCycle(7.5)  # Return arm to neutral
        elif action == "dropoff":
            print("Dropping off object")
            self.arm_pwm.ChangeDutyCycle(5)  # Rotate arm to position
            time.sleep(1)
            self.grip_pwm.ChangeDutyCycle(7.5)  # Open grip
            time.sleep(1)
            self.arm_pwm.ChangeDutyCycle(7.5)  # Return arm to neutral

    def run(self):
        while True:
            if GPIO.input(self.distance_sensor_gpio):
                self.distance_sensor_triggered += 1
                if self.distance_sensor_triggered == 1:
                    self.stop()
                    self.handle_object("pickup")
                elif self.distance_sensor_triggered == 2:
                    self.stop()
                    self.handle_object("dropoff")
                    break  # End operation after drop-off

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
                if GPIO.input(self.distance_sensor_gpio):
                    if self.distance_sensor_triggered < 2:
                        self.state = "OBJECT_DETECTED"
                    else:
                        self.state = "DROPPING_OFF"

            time.sleep(0.1)  # Small delay to prevent excessive CPU usage

if __name__ == "__main__":
    try:
        sav = SAV()
        sav.run()
    except KeyboardInterrupt:
        print("Cleanup")
        GPIO.cleanup()
