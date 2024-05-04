import RPi.GPIO as GPIO
import time

# Define GPIO pin numbers for data and clock lines
DATA_Pin = 21  # GPIO pin for data (DATA)
CLK_Pin = 20   # GPIO pin for clock (CLK)

# Define command and data values for LED bar control
CmdMode = 0x0000  # Command mode (work on 8-bit mode)
ON = 0x00ff       # Data to turn on LEDs (8-byte 1 data)
SHUT = 0x0000     # Data to turn off LEDs (8-byte 0 data)

# Global variable to track clock signal state
global s_clk_flag
s_clk_flag = 0

def send16bitData(data):
    global s_clk_flag
    # Send 16 bits of data (MSB first)
    for i in range(0, 16):
        if data & 0x8000:
            GPIO.output(DATA_Pin, GPIO.HIGH)
        else:
            GPIO.output(DATA_Pin, GPIO.LOW)
        
        # Toggle clock signal (rising edge-triggered)
        if s_clk_flag == True:
            GPIO.output(CLK_Pin, GPIO.LOW)
            s_clk_flag = 0
        else:
            GPIO.output(CLK_Pin, GPIO.HIGH)
            s_clk_flag = 1
        
        # Shift data to the left by 1 bit
        data = data << 1
        time.sleep(0.001)  # Delay to control clock frequency

def latchData():
    latch_flag = 0
    GPIO.output(DATA_Pin, GPIO.LOW)
    
    # Pulse latch signal to latch the data
    time.sleep(0.05)
    for i in range(0, 8):
        if latch_flag == True:
            GPIO.output(DATA_Pin, GPIO.LOW)
            latch_flag = 0
        else:
            GPIO.output(DATA_Pin, GPIO.HIGH)
            latch_flag = 1
        time.sleep(0.05)

def sendLED(LEDstate):
    # Send LED state data (12 bits) to the LED bar
    for i in range(0, 12):
        if (LEDstate & 0x0001) == True:
            send16bitData(ON)
        else:
            send16bitData(SHUT)
        LEDstate = LEDstate >> 1

def setup():
    print("Adeept LED bar test code!")
    print("Using DATA = PIN21(GPIO9), CLK = PIN20(GPIO10)")

    # Set up GPIO pins for output
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(DATA_Pin, GPIO.OUT)
    GPIO.setup(CLK_Pin, GPIO.OUT)

    GPIO.output(DATA_Pin, GPIO.LOW)
    GPIO.output(CLK_Pin, GPIO.LOW)

def loop():
    # Continuous loop to control the LED bar display
    while True:
        i = 0x0000
        # Cycle through LED states from 0x0000 to 0x03ff (12 LEDs)
        while i <= 0x03ff:
            send16bitData(CmdMode)  # Send command mode
            sendLED(i)               # Send LED state data
            latchData()              # Latch the data to update LED display
            i = i * 2 + 1            # Increment LED state
            time.sleep(0.1)          # Delay between LED state changes

def destroy():
    # Clean up GPIO on program exit
    GPIO.cleanup()

# Main function to set up and run the LED bar control
if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
