import RPi.GPIO as GPIO
import time

# Define GPIO pin for the passive buzzer
PBUZZER = 22

# Set GPIO mode and configure buzzer pin as output
GPIO.setmode(GPIO.BCM)
GPIO.setup(PBUZZER, GPIO.OUT)

# Initialize buzzer pin to LOW (off) initially
GPIO.output(PBUZZER, GPIO.LOW)

# Create PWM object for the buzzer with an initial frequency of 50Hz and 50% duty cycle
p = GPIO.PWM(PBUZZER, 50)  # Initialize PWM with frequency: 50Hz
p.start(50)                 # Start PWM with duty cycle: 50%

try:
    # Infinite loop to generate varying frequencies
    while True:
        # Increasing frequency from 100Hz to 2000Hz in steps of 100Hz
        for f in range(100, 2000, 100):
            p.ChangeFrequency(f)  # Change PWM frequency to f Hz
            time.sleep(0.2)       # Wait for 0.2 seconds (adjust as needed)

        # Decreasing frequency from 2000Hz to 100Hz in steps of -100Hz
        for f in range(2000, 100, -100):
            p.ChangeFrequency(f)  # Change PWM frequency to f Hz
            time.sleep(0.2)       # Wait for 0.2 seconds (adjust as needed)

except KeyboardInterrupt:
    # Clean up GPIO and stop PWM on keyboard interrupt (Ctrl+C)
    p.stop()         # Stop PWM
    GPIO.cleanup()   # Clean up GPIO resources

