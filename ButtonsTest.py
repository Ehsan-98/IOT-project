import RPi.GPIO as GPIO
import time

# Set the GPIO pin numbering mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pins for the buttons
button_pin_1 = 5
button_pin_2 = 6

# Setup the button pins as inputs with internal pull-up resistors
GPIO.setup(button_pin_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_pin_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

button_pressed_1 = False  # Flag to track button 1 press state
button_pressed_2 = False  # Flag to track button 2 press state

try:
    while True:
        # Check if button 1 is pressed (button_pin_1 is LOW)
        if GPIO.input(button_pin_1) == GPIO.LOW:
            if not button_pressed_1:  # Check if button 1 was just pressed
                print("Button 1 is pressed!")
                button_pressed_1 = True  # Set button 1 pressed flag
        else:
            button_pressed_1 = False  # Reset button 1 pressed flag when button 1 is released

        # Check if button 2 is pressed (button_pin_2 is LOW)
        if GPIO.input(button_pin_2) == GPIO.LOW:
            if not button_pressed_2:  # Check if button 2 was just pressed
                print("Button 2 is pressed!")
                button_pressed_2 = True  # Set button 2 pressed flag
        else:
            button_pressed_2 = False  # Reset button 2 pressed flag when button 2 is released
        
        # Add a small delay to debounce the buttons
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Cleaning up...")
    GPIO.cleanup()

