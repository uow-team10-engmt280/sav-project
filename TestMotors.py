import time as t
import RPi.GPIO as GPIO # type: ignore

phaseA: int = 5
enableA: int = 12
phaseB: int = 19
enableB: int = 13

driveMode: int = 1

GPIO.setmode(GPIO.BCM)

GPIO.setup(driveMode, GPIO.OUT)
GPIO.output(driveMode, GPIO.HIGH)

GPIO.setup(phaseA, GPIO.OUT)
GPIO.setup(enableA, GPIO.OUT) 
GPIO.setup(phaseB, GPIO.OUT)
GPIO.setup(enableB, GPIO.OUT) 

GPIO.output(phaseA, GPIO.LOW)
GPIO.output(enableA, GPIO.LOW)
GPIO.output(phaseB, GPIO.LOW)
GPIO.output(enableB, GPIO.LOW)

pwmA = GPIO.PWM(enableA, 1000)
pwmB = GPIO.PWM(enableB, 1000)

pwmA.start(0)
pwmB.start(0)

while True:
    GPIO.output(phaseA, GPIO.HIGH)
    pwmA.ChangeDutyCycle(0.05)
    GPIO.output(phaseB, GPIO.HIGH)
    pwmB.ChangeDutyCycle(0.05)
    if t.time() < 10:
        break

pwmA.stop()
pwmB.stop()

GPIO.cleanup()

