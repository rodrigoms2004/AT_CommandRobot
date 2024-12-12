import RPi.GPIO as GPIO
import time

in1 = 16 # gpio 23

GPIO.setmode(GPIO.BOARD)
GPIO.setup(in1, GPIO.OUT)

GPIO.output(in1, False)

try:
    GPIO.output(in1, True)
    time.sleep(1)
    GPIO.output(in1, False)

except KeyboardInterrupt:
    GPIO.cleanup()

