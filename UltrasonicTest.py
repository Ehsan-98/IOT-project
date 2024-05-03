import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

pindistance1 = 23
pindistance2 = 24

def checkdist():
    GPIO.output(pindistance1, GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(pindistance1, GPIO.LOW)
    while not GPIO.input(pindistance2):
        pass
    t1 = time.time()
    while GPIO.input(pindistance2):
        pass
    t2 = time.time()
    return (t2 - t1) * 340 / 2

GPIO.setmode(GPIO.BCM)

GPIO.setup(pindistance1, GPIO.OUT)
GPIO.setup(pindistance2,GPIO.IN)
time.sleep(2)
try:
    while True:
        print('Distance: %0.2f cm' %checkdist())
        time.sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()
