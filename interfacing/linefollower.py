import time
import RPi.GPIO as GPIO
from linesensor import LineSensor


def calc_error(sensor_values):
    weights = [-8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8]
    error_total = 0
    total_weighted = 0

    for channel, value in enumerate(sensor_values):
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

def detect_fork(sensor_values):
    for i in range(4):
        total_lft += sensor_values[i]

    for j in range(4):
        total_rgt += sensor_values[9 - j]

    if total_lft >= 2 and total_rgt >= 2:
        return "at fork"
    else:
        return "no fork"

try:    
    sensor = LineSensor()
    sensor_values = sensor.read()
    calc_error(sensor_values)
finally:
    GPIO.cleanup()