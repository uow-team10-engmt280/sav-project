# Read line Sensor info a 9 bit binary number from aother module, moves or turns accordingly

# Whilst moving if the distance sensor gpio goes high stop and turn servo and pickup object, then give the line sensor a timeout, allowing the sav to move even if its high for a time period. 
# Motor controller sets speed higher when moving normally, and for turning its slower

# Once line Sensor detects binary for parking, the sav stops moving

# States are in while loop
#
import time

class SAV:
    def __init__(self):
        self.state = "START"
        self.line_sensor_data = 0b000000000  # 9-bit binary number
        self.distance_sensor_gpio = False
        self.parking_binary = 0b100000001  # Example parking binary pattern
        self.timeout_duration = 5  # Timeout duration in seconds
        self.motor_speed_normal = 100  # Normal movement speed
        self.motor_speed_turn = 50  # Turning speed
        self.timeout_start = None

    def read_line_sensor(self):
        # This function would interface with the hardware to read the 9-bit binary number from the line sensor
        pass

    def check_distance_sensor(self):
        # This function would interface with the hardware to check the distance sensor GPIO status
        pass

    def move(self):
        # Code to set the motor speed to normal and move forward
        print("Moving forward at normal speed")

    def turn(self):
        # Code to set the motor speed to turning speed and turn
        print("Turning at reduced speed")

    def stop(self):
        # Code to stop the motors
        print("Stopping")

    def pickup_object(self):
        # Code to control servo and pick up object
        print("Picking up object")

    def line_sensor_timeout(self):
        # Check if timeout has started
        if self.timeout_start is None:
            self.timeout_start = time.time()
        
        # Check if timeout duration has passed
        if time.time() - self.timeout_start > self.timeout_duration:
            self.timeout_start = None  # Reset timeout
            return True
        return False

    def update_state(self):
        self.read_line_sensor()
        self.check_distance_sensor()

        if self.state == "START":
            self.move()
            if self.distance_sensor_gpio:
                self.state = "OBJECT_DETECTED"
            elif self.line_sensor_data == self.parking_binary:
                self.state = "PARKED"

        elif self.state == "OBJECT_DETECTED":
            self.stop()
            self.pickup_object()
            self.state = "TIMEOUT"

        elif self.state == "TIMEOUT":
            if self.line_sensor_timeout():
                self.state = "MOVING_AGAIN"

        elif self.state == "MOVING_AGAIN":
            self.move()
            if self.line_sensor_data == self.parking_binary:
                self.state = "PARKED"
            elif self.distance_sensor_gpio:
                self.state = "OBJECT_DETECTED"

        elif self.state == "PARKED":
            self.stop()
            print("SAV is parked.")

    def run(self):
        while True:
            self.update_state()
            time.sleep(0.1)  # Small delay to prevent excessive CPU usage

if __name__ == "__main__":
    sav = SAV()
    sav.run()
