from FindCase import FindCase
from RPi import GPIO # type: ignore
import the sensor programme

# Initialise values



try:
    while True:
        FindCase()
except:
    GPIO.cleanup()