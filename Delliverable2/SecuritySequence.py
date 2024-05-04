import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Define GPIO pins for buttons and LEDs
button_pin_blue = 5   # Blue button
button_pin_red = 6    # Red button
green_led_pin = 19    # Green LED
red_led_pin = 26      # Red LED

# Setup GPIO for buttons (with internal pull-up resistors)
GPIO.setup(button_pin_blue, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_pin_red, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Setup GPIO for LEDs
GPIO.setup(green_led_pin, GPIO.OUT)
GPIO.setup(red_led_pin, GPIO.OUT)

# Define the correct sequence of button presses (BLUE-RED-BLUE)
correct_sequence = [button_pin_blue, button_pin_red, button_pin_blue]

# Initialize variables for tracking button presses
current_sequence = []
sequence_start_time = None

def reset_sequence():
    global current_sequence
    current_sequence = []
    GPIO.output(green_led_pin, GPIO.LOW)
    GPIO.output(red_led_pin, GPIO.LOW)

try:
    while True:
        # Check for button presses
        if GPIO.input(button_pin_blue) == GPIO.LOW:
            current_sequence.append(button_pin_blue)
            time.sleep(0.2)  # Debounce delay
        elif GPIO.input(button_pin_red) == GPIO.LOW:
            current_sequence.append(button_pin_red)
            time.sleep(0.2)  # Debounce delay
        
        # Check if the current sequence matches the correct sequence
        if len(current_sequence) == len(correct_sequence):
            if current_sequence == correct_sequence:
                # Correct sequence entered
                print("Correct sequence entered!")
                GPIO.output(green_led_pin, GPIO.HIGH)  # Turn on green LED
                time.sleep(1)  # LED indication time
                reset_sequence()  # Reset sequence and LEDs
            else:
                # Incorrect sequence entered
                print("Incorrect sequence entered!")
                GPIO.output(red_led_pin, GPIO.HIGH)  # Turn on red LED
                time.sleep(1)  # LED indication time
                reset_sequence()  # Reset sequence and LEDs
        
        # Check if more than 4 seconds have passed without completing the sequence
        if sequence_start_time and (time.time() - sequence_start_time > 4):
            print("Timeout - Sequence reset")
            reset_sequence()  # Reset sequence and LEDs
            sequence_start_time = None
        
        # Check if sequence start time needs to be initialized
        if not sequence_start_time and len(current_sequence) > 0:
            sequence_start_time = time.time()
        
        time.sleep(0.1)  # Polling interval

except KeyboardInterrupt:
    print("Cleaning up...")
    GPIO.cleanup()

