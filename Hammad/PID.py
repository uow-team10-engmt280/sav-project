# main.py

import time
import sensor_module

# PID control parameters
Kp = 1.0  # Proportional gain
Ki = 0.0  # Integral gain
Kd = 0.0  # Derivative gain

# Global variables for PID
previous_error = 0
integral = 0

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
    # The position is calculated as a weighted sum of sensor indices
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
    # This function would implement the motor control based on the PID output
    base_speed = 50  # Base speed for motors
    left_motor_speed = base_speed - pid_output
    right_motor_speed = base_speed + pid_output

    # Limit motor speed to between 0 and 100
    left_motor_speed = max(0, min(100, left_motor_speed))
    right_motor_speed = max(0, min(100, right_motor_speed))

    # Print motor speeds for debugging (replace with actual motor control code)
    print(f"Left motor speed: {left_motor_speed}, Right motor speed: {right_motor_speed}")

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

if __name__ == "__main__":
    main()
