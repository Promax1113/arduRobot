# DEPRECATED #
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)

while True:
    GPIO.output(5, True)
    print("Light")
    GPIO.output(5, False)
    print("not light")
