import RPi.GPIO as GPIO
import time


class Motor:
    def __init__(self, motor_pins: list[int], mode = 1):
        GPIO.setmode(GPIO.BCM)

        # set pins as output
        GPIO.setup(motor_pins, GPIO.OUT)
        
        # setup pwm on the pins
        self.in_1_pwm = GPIO.PWM(motor_pins[0], 50) # starting freq @ 50 Hz
        self.in_2_pwm = GPIO.PWM(motor_pins[1], 50) # starting freq @ 50 Hz

        # start pwm signal with 0% duty cycle
        self.in_1_pwm.start(0.0)
        self.in_2_pwm.start(0.0)


    def coast(self):
        # in_1 -> 0
        # in_2 -> 0

        self.in_1_pwm.stop()
        self.in_2_pwm.stop()

        GPIO.output(self.motor_pins, GPIO.HIGH)


    def forward(self, speed: float):
        self.in_1_pwm.stop()
        self.in_2_pwm.stop()
        # in_1 -> PWM = SPEED
        # in_2 -> 1

        # intial value at 0
        self.in_1_pwm.start(0.0)
        self.in_2_pwm.start(0.0)

        self.in_2_pwm.stop()
        
        GPIO.output(self.motor_pins[1], GPIO.HIGH)

        self.in_1_pwm.ChangeDutyCycle(speed)

    def reverse(self, speed: float):
        self.in_1_pwm.stop()
        self.in_2_pwm.stop()
        # in_1 -> 1
        # in_2 -> PWM = SPEED

        # intial value at 0
        self.in_1_pwm.start(0.0)
        self.in_2_pwm.start(0.0)

        self.in_1_pwm.stop()
        
        GPIO.output(self.motor_pins[0], GPIO.HIGH)

        self.in_2_pwm.ChangeDutyCycle(speed)


    def brake(self):
        # in_1 -> 1
        # in_2 -> 1
        self.in_1_pwm.stop()
        self.in_2_pwm.stop()
        
        GPIO.output(self.motor_pins, GPIO.HIGH)

    def cleanup(self):
        self.in_1_pwm.stop()
        self.in_2_pwm.stop()

        GPIO.cleanup(self.motor_pins)

if __name__ == "__main__":
    motor_pins_0 = [5, 12] # Phase, Enable / In 1, In 2
    motor_pins_1 = [19, 13] # Phase, Enable / In 1, In 2
    mode_pin = 0

    motor_lft = Motor(motor_pins_0)
    motor_rgt = Motor(motor_pins_1)

    while True:
        motor_lft.forward(50)
        motor_rgt.forward(50)
        time.sleep(2)
        
        break

    motor_lft.brake()
    motor_rgt.brake()
    time.sleep(2)

    while True:
        motor_lft.reverse(30)
        motor_rgt.reverse(30)
        time.sleep(2)

        break

    motor_lft.cleanup()
    motor_rgt.cleanup()