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
        # Simulate reading line sensor
        pass

    def check_distance_sensor(self):
        # If sensor is high transition to stop and then pickup left or right based on camera
        pass

    def move(self):
        # Simulate moving forward
        # If line sensor needs to turn, stop 
        print("Moving forward at normal speed")

    def turn(self):
        # Adjust the position, move, straighten out and then go back into default move state
        print("Turning at reduced speed")

    def stop(self):
        # If stopped and distance sensor is high, transition to pickup_obkect
        # IF line sensor says to turn go into turning state
        print("Stopping")

    def pickup_object(self):
        # Based on camera input information, rotate arm left or right
        # Close the grip
        # Rotate arm into original position
        # Resume Move state
        print("Picking up object")

    def dropoff_object(self):
        # Based on camera input information, rotate arm left or right
        # Open the grip
        # Rotate arm into original position
        # Resume Move state
        print("Dropping off object")

    def line_sensor_timeout(self):
        # Handle line sensor timeout
        if self.timeout_start is None:
            self.timeout_start = time.time()
        if time.time() - self.timeout_start > self.timeout_duration:
            self.timeout_start = None  # Reset timeout
            return True
        return False

    def run(self):
        while True:
            self.read_line_sensor()
            self.check_distance_sensor()

            match self.state:
                case "START":
                    self.move()
                    if self.distance_sensor_gpio:
                        self.state = "OBJECT_DETECTED"
                    elif self.line_sensor_data == self.parking_binary:
                        self.state = "PARKED"

                case "OBJECT_DETECTED":
                    self.stop()
                    self.pickup_object()
                    self.state = "TIMEOUT"

                case "TIMEOUT":
                    if self.line_sensor_timeout():
                        self.state = "MOVING_AGAIN"

                case "MOVING_AGAIN":
                    self.move()
                    if self.line_sensor_data == self.parking_binary:
                        self.state = "PARKED"
                    elif self.distance_sensor_gpio:
                        self.state = "OBJECT_DETECTED"

                case "PARKED":
                    self.stop()
                    print("SAV is parked.")
                    break  # Exit the loop once parked

            time.sleep(0.1)  # Small delay to prevent excessive CPU usage

if __name__ == "__main__":
    sav = SAV()
    sav.run()
