from time import time, sleep
import RPi.GPIO as GPIO

# Setup GPIO
GPIO.setmode(GPIO.BCM)  # Or GPIO.BOARD, depending on your pin numbering preference
# GPIO.setup(sensor_pins, GPIO.IN)  # Setup sensor pins here
# GPIO.setup(motor_pins, GPIO.OUT)  # Setup motor control pins here

# Define global variables and flags
movPhase = 'phaseFork'
forkFlag = False
pickDropFlag = False
mergeFlag = False
motorDriverMode = False
startTime = 0

# Define the SAV class which holds the state management methods
class SAV:
    def __init__(self):
        self.state = 'IDLE'

    def idle(self):
        print("Entering IDLE state")
        while True:
            command = input('Type "Start" to begin the program when you\'re ready: \n').lower()
            if command in ['s', 'start']:
                self.state = 'LISTENING'
                break
            else:
                print('Invalid, try again. \n')

    def listening(self):
        print('Entered LISTENING state successfully. \n')
        global startTime
        startTime = time()

        # Placeholder: Replace with actual function to get sensor data
        TParray = self.get_sensor_data()

        self.turnOne = TParray[0]
        self.pickUpSideOne = TParray[1]
        self.turnTwo = TParray[2]
        self.pickUpSideTwo = TParray[3]

        while True:
            command = input('Decisions received, type "Next" to start race: \n').lower()
            if command in ['n', 'next']:
                self.state = 'MOVING'
                break
            else:
                print('Invalid, try again. \n')

    def get_sensor_data(self):
        # Replace this function with actual sensor data collection logic
        return [0, 1, 0, 1]  # Example data

    def moving(self):
        global forkFlag, pickDropFlag, mergeFlag

        print('Entered MOVING state successfully. \n')

        while True:
            if movPhase == 'phaseFork':
                if not forkFlag:
                    pass  # Implement movement logic
                else:
                    pass  # Implement logic for after the fork
            elif movPhase == 'phasePickDrop':
                if not pickDropFlag:
                    pass  # Implement pick/drop movement logic
                else:
                    pass  # Implement logic for after pick/drop
                break
            elif movPhase == 'phaseMerge':
                if not mergeFlag:
                    pickDropFlag = True
                else:
                    pass  # Implement merging logic
                break
            elif movPhase == 'phasePark':
                break  # Implement parking logic

        if not pickDropFlag:
            self.state = 'PICKUP'
        else:
            self.state = 'DROPOFF'

    def pickup(self):
        print('Entered PICKUP state successfully. \n')
        # Implement the pickup logic
        self.state = 'MOVING'

    def dropoff(self):
        print('Entered DROPOFF state successfully. \n')
        # Implement the dropoff logic
        self.state = 'MOVING'

    def parking(self):
        print('Entered PARKING state successfully. \n')
        # Implement parking logic
        self.state = 'COMPLETE'

    def complete(self):
        print('Entered COMPLETE state successfully.')
        endTime = time()
        raceTime = endTime - startTime
        minutes = raceTime // 60
        seconds = raceTime % 60
        print(f'You took {int(minutes)} minutes and {seconds:.2f} seconds to complete the track.')
        # Implement any finalization logic like playing a sound or stopping all motors
        # End the program or restart

    def run(self):
        while True:
            if self.state == 'IDLE':
                self.idle()
            elif self.state == 'LISTENING':
                self.listening()
            elif self.state == 'MOVING':
                self.moving()
            elif self.state == 'PICKUP':
                self.pickup()
            elif self.state == 'DROPOFF':
                self.dropoff()
            elif self.state == 'PARKING':
                self.parking()
            elif self.state == 'COMPLETE':
                self.complete()
                break

# Main execution
def main() -> None:
    sav = SAV()
    sav.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Program interrupted and GPIO cleaned up.")
