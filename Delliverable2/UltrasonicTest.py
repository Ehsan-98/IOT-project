import RPi.GPIO as GPIO
import time

# Suppress GPIO warnings (optional)
GPIO.setwarnings(False)

# Define GPIO pin numbers for ultrasonic sensor (trigger and echo)
pindistance1 = 23  # GPIO pin for trigger (TRIG)
pindistance2 = 24  # GPIO pin for echo (ECHO)

def checkdist():
    # Send a 10us HIGH pulse to trigger the ultrasonic sensor
    GPIO.output(pindistance1, GPIO.HIGH)
    time.sleep(0.000015)  # Wait for 15 microseconds
    GPIO.output(pindistance1, GPIO.LOW)

    # Measure the duration of the ECHO signal
    while not GPIO.input(pindistance2):
        pass
    t1 = time.time()  # Record the start time of the ECHO signal

    while GPIO.input(pindistance2):
        pass
    t2 = time.time()  # Record the end time of the ECHO signal

    # Calculate distance based on the time difference (in seconds) and speed of sound (340 m/s)
    distance = (t2 - t1) * 340 / 2  # Calculate distance in centimeters
    return distance

# Set GPIO mode to BCM (Broadcom SOC channel numbering)
GPIO.setmode(GPIO.BCM)

# Set up GPIO pins for ultrasonic sensor (TRIG as output, ECHO as input)
GPIO.setup(pindistance1, GPIO.OUT)  # TRIG
GPIO.setup(pindistance2, GPIO.IN)   # ECHO

time.sleep(2)  # Allow sensor to settle

try:
    # Infinite loop to continuously measure and print distance
    while True:
        distance = checkdist()  # Call the function to measure distance
        print('Distance: %0.2f cm' % distance)  # Print distance with 2 decimal places
        time.sleep(0.5)  # Delay between distance measurements

except KeyboardInterrupt:
    # Clean up GPIO settings on keyboard interrupt (Ctrl+C)
    GPIO.cleanup()
