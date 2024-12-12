import RPi.GPIO as GPIO
import time

in1 = 16 # gpio 23

def restart(delay):

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(in1, GPIO.OUT)

    GPIO.output(in1, False)

    try:
        GPIO.output(in1, True)
        time.sleep(delay)
        GPIO.output(in1, False)

    except KeyboardInterrupt:
        GPIO.cleanup()
