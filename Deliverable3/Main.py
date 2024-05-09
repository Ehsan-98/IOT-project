import tkinter as tk
from tkinter import ttk, messagebox
import RPi.GPIO as GPIO
import time
import threading
import sys

# GPIO pin assignments for trash level monitoring
TRIGGER_PIN = 23
ECHO_PIN = 24

# GPIO pin assignments for security system
button_pin_blue = 5   # Blue button
button_pin_red = 6    # Red button
green_led_pin = 19    # Green LED
red_led_pin = 26      # Red LED

# Buzzer pin for lid alarm
PBUZZER = 22

# Set up GPIO 
# Set GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# GPIO pin assignments for trash level monitoring
GPIO.setup(TRIGGER_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

# Set up GPIO for security system
GPIO.setup(button_pin_blue, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_pin_red, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(green_led_pin, GPIO.OUT)
GPIO.setup(red_led_pin, GPIO.OUT)

# Set up GPIO for lid alarm (buzzer)
GPIO.setup(PBUZZER, GPIO.OUT)
GPIO.output(PBUZZER, GPIO.LOW)

# Calibration values (measured distances in cm)
empty_distance = 3.03  # Distance when the container is empty (in cm)
full_distance = 4.32   # Distance when the container is full of trash (in cm)

# Threshold percentage for garbage bin capacity
threshold_percentage = 40 # Default threshold value (80%)

# Variables for system state
locked = True  # System starts in locked state

# Function to measure distance using ultrasonic sensor
def measure_distance():
    GPIO.output(TRIGGER_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIGGER_PIN, False)

    pulse_start = time.time()
    pulse_end = time.time()

    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = (pulse_duration * 34300) / 2  # Calculate distance in cm (speed of sound = 343 m/s)
    return distance

# Function to estimate trash level percentage based on distance
def estimate_trash_level(distance):
    if distance <= empty_distance:
        trash_percentage = 0.0
    elif distance >= full_distance:
        trash_percentage = 100.0
    else:
        trash_range = full_distance - empty_distance
        distance_from_empty = distance - empty_distance
        trash_percentage = (distance_from_empty / trash_range) * 100

    return trash_percentage

# Function to handle setting the trash threshold
def set_threshold():
    global threshold_percentage
    new_threshold = int(entry_threshold.get())
    if 0 <= new_threshold <= 100:
        threshold_percentage = new_threshold
        label_threshold.config(text=f"Threshold set to {threshold_percentage}%")
    else:
        label_threshold.config(text="Invalid threshold (0-100)")

# Function to handle the security system logic
def security_system():
    global locked
    correct_sequence = [button_pin_blue, button_pin_red, button_pin_blue]
    current_sequence = []
    sequence_start_time = None
    timeout_printed = False  # Flag to track if timeout message has been printed

    def reset_sequence():
        nonlocal current_sequence, timeout_printed
        current_sequence = []
        GPIO.output(green_led_pin, GPIO.LOW)
        GPIO.output(red_led_pin, GPIO.LOW)
        timeout_printed = False  # Reset the timeout flag

    try:
        while True:
            if GPIO.input(button_pin_blue) == GPIO.LOW:
                current_sequence.append(button_pin_blue)
                time.sleep(0.2)  # Debounce delay
            elif GPIO.input(button_pin_red) == GPIO.LOW:
                current_sequence.append(button_pin_red)
                time.sleep(0.2)  # Debounce delay

            if len(current_sequence) >= len(correct_sequence):
                if current_sequence == correct_sequence:
                    # Correct sequence entered
                    print("Correct sequence entered!")
                    GPIO.output(green_led_pin, GPIO.HIGH)  # Turn on green LED
                    time.sleep(1)  # LED indication time
                    reset_sequence()  # Reset sequence and LEDs
                    locked = False  # Unlock the system
                else:
                    # Incorrect sequence entered
                    print("Incorrect sequence entered!")
                    GPIO.output(red_led_pin, GPIO.HIGH)  # Turn on red LED
                    time.sleep(1)  # LED indication time
                    reset_sequence()  # Reset sequence and LEDs

            if sequence_start_time and (time.time() - sequence_start_time > 4) and not timeout_printed:
                print("Timeout - Sequence reset")
                reset_sequence()  # Reset sequence and LEDs
                timeout_printed = True  # Set the flag to indicate timeout message printed

            if not sequence_start_time and len(current_sequence) > 0:
                sequence_start_time = time.time()

            time.sleep(0.1)  # Polling interval

    except KeyboardInterrupt:
        print("Cleaning up...")
        GPIO.cleanup()

# Function to handle GUI updates
def update_gui():
    if not locked:
        distance = measure_distance()
        trash_percentage = estimate_trash_level(distance)
        trash_level_label.config(text=f"Trash Level: {trash_percentage:.2f}%")

        if trash_percentage > threshold_percentage:
            trash_level_label.config(foreground="red")
        else:
            trash_level_label.config(foreground="black")

    if locked:
        system_status_label.config(text="System Status: Locked", foreground="red")
    else:
        system_status_label.config(text="System Status: Unlocked", foreground="green")

    root.after(500, update_gui)  # Schedule the next update

# Function to check lid status and activate/deactivate alarm
def check_lid():
    try:
        lid_closed = True  # Assume lid is initially closed

        while True:
            distance = measure_distance()
            if distance > 6.0:  # Adjust this threshold based on your setup
                if lid_closed:
                    # Lid has been opened
                    print("Lid opened - activating buzzer")
                    p.ChangeFrequency(1000)  # Set buzzer frequency
                    p.ChangeDutyCycle(50)    # Set buzzer duty cycle to 50%
                    lid_closed = False
                    # Show warning dialog for lid open
                    messagebox.showwarning("Warning", "Lid is open!")
            else:
                if not lid_closed:
                    # Lid has been closed
                    print("Lid closed - deactivating buzzer")
                    p.ChangeDutyCycle(0)  # Turn off the buzzer
                    lid_closed = True

            time.sleep(0.5)  # Adjust the polling interval as needed

    except KeyboardInterrupt:
        # Clean up GPIO settings on Ctrl+C exit
        p.stop()
        GPIO.cleanup()

# Function to clean up GPIO and exit the application
def exit_application():
    GPIO.cleanup()
    sys.exit(0)  # Exit the application

# Create main GUI window
root = tk.Tk()
root.title("Smart Waste Management System")

# Create label to display trash level percentage
trash_level_label = ttk.Label(root, text="Trash Level: ---%", font=("Helvetica", 18))
trash_level_label.pack(pady=20)

# Create entry field to set the waste threshold
entry_threshold = ttk.Entry(root, width=10, font=("Helvetica", 12))
entry_threshold.insert(0, str(threshold_percentage))  # Display default threshold value
entry_threshold.pack(pady=10)

# Create button to set the threshold
button_set_threshold = ttk.Button(root, text="Set Threshold", command=set_threshold)
button_set_threshold.pack(pady=10)

# Label to display the current threshold setting
label_threshold = ttk.Label(root, text=f"Threshold set to {threshold_percentage}%", font=("Helvetica", 12))
label_threshold.pack(pady=10)

# Label to display system status
system_status_label = ttk.Label(root, text="System Status: Locked", font=("Helvetica", 12), foreground="red")
system_status_label.pack(pady=10)

# Button to exit the application
button_exit = ttk.Button(root, text="Exit", command=exit_application)
button_exit.pack(pady=10)

# Start threads for security system, GUI updates, and lid detection
security_thread = threading.Thread(target=security_system)
gui_update_thread = threading.Thread(target=update_gui)
lid_detection_thread = threading.Thread(target=check_lid)


# Initialize PWM for buzzer
p = GPIO.PWM(PBUZZER, 1000)  # Set PWM frequency to 1000 Hz
p.start(0)  # Start PWM with 0% duty cycle


security_thread.start()
gui_update_thread.start()
lid_detection_thread.start()

# Run the main GUI event loop
root.mainloop()

