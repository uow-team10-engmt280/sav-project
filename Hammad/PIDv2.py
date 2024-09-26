import time
import sensor_module
import RPi.GPIO as GPIO

# PID control parameters
Kp = 1.0  # Proportional gain
Ki = 0.0  # Integral gain
Kd = 0.0  # Derivative gain

# Global variables for PID
previous_error = 0
integral = 0

# Motor control pin definitions
LEFT_MOTOR_ENABLE = 23  # GPIO pin for left motor enable
RIGHT_MOTOR_ENABLE = 24  # GPIO pin for right motor enable
LEFT_MOTOR_PHASE = 17    # GPIO pin for left motor direction
RIGHT_MOTOR_PHASE = 27   # GPIO pin for right motor direction

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(LEFT_MOTOR_ENABLE, GPIO.OUT)
GPIO.setup(RIGHT_MOTOR_ENABLE, GPIO.OUT)
GPIO.setup(LEFT_MOTOR_PHASE, GPIO.OUT)
GPIO.setup(RIGHT_MOTOR_PHASE, GPIO.OUT)

def calculate_pid(error, dt):
    global previous_error, integral

    # Proportional term
    P = Kp * error

    # Integral term
    integral += error * dt
    I = Ki * integral

    # Derivative term
    derivative = (error - previous_error) / dt
    D = Kd * derivative

    # PID output
    pid_output = P + I + D

    # Update previous error
    previous_error = error

    return pid_output

def determine_position(sensor_list):
    # Define the setpoint (desired position), usually the middle of the track
    setpoint = 4  # Middle of a 9-sensor array

    # Calculate position error based on sensor readings
    if sum(sensor_list) > 0:
        position = sum([i for i, val in enumerate(sensor_list) if val == 1]) / sum(sensor_list)
    else:
        position = setpoint  # Default to setpoint if no sensor is detecting

    error = setpoint - position

    # Calculate the time step for the PID loop
    dt = 0.01  # Adjust this based on loop speed

    # Calculate PID output
    pid_output = calculate_pid(error, dt)

    # Apply the PID output to control motor speeds
    control_motors(pid_output)

def control_motors(pid_output):
    base_speed = 100  # Maximum speed for motors (100%)
    left_motor_speed = base_speed - pid_output
    right_motor_speed = base_speed + pid_output

    # Limit motor speed to between 0 and 100
    left_motor_speed = max(0, min(100, left_motor_speed))
    right_motor_speed = max(0, min(100, right_motor_speed))

    # Set motor direction based on speed values
    GPIO.output(LEFT_MOTOR_PHASE, GPIO.HIGH if left_motor_speed > 0 else GPIO.LOW)
    GPIO.output(RIGHT_MOTOR_PHASE, GPIO.HIGH if right_motor_speed > 0 else GPIO.LOW)

    # Enable motors
    GPIO.output(LEFT_MOTOR_ENABLE, GPIO.HIGH)
    GPIO.output(RIGHT_MOTOR_ENABLE, GPIO.HIGH)

    # Print motor speeds for debugging (replace with actual motor control code)
    print(f"Left motor speed: {left_motor_speed}, Right motor speed: {right_motor_speed}")

def stop_motors():
    GPIO.output(LEFT_MOTOR_ENABLE, GPIO.LOW)
    GPIO.output(RIGHT_MOTOR_ENABLE, GPIO.LOW)

def main():
    try:
        # Initialize the control loop
        while True:
            # Get sensor outputs from the sensor module
            sensor_outputs = sensor_module.get_sensor_outputs()
            
            # Determine position and control motors
            determine_position(sensor_outputs)

            # Add a small delay to avoid overwhelming the CPU
            time.sleep(0.01)

    except KeyboardInterrupt:
        # Handle a clean exit on user interruption (Ctrl + C)
        print("Exiting program")
    finally:
        stop_motors()
        GPIO.cleanup()

if __name__ == "__main__":
    main()
