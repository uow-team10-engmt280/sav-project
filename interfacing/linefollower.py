import time
import RPi.GPIO as GPIO
from linesensor import LineSensor


def calc_error(LineSensor):
    weights = [-8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8]
    error_total = 0
    total_weighted = 0

    for channel, value in enumerate(LineSensor.sensor_values):
        if value == 1:
            error_total += weights[channel]
            total_weighted += 1

    error = error_total / total_weighted

    if error > 0:
        return error
    else:
        return None
    
# def pid_controller(error, dt):
#     global integral, previous_error

#     proportional = Kp * error
#     integral += error * dt
#     derivative = (error - previous_error) / dt
#     previous_error = error

#     return proportional + (Ki * integral) + (Kd * derivative)