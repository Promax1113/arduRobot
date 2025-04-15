import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)

while True:
    GPIO.output(5, True)
    time.sleep(1)
    GPIO.output(5, False)
    time.sleep(1)
