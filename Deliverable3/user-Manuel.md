
Smart Waste Management System User Manual
Welcome to the Smart Waste Management System! This system is designed to monitor trash levels in a waste container and provide security features to control access to the system.

System Overview:
The Smart Waste Management System utilizes ultrasonic sensors to measure the trash level inside a waste container. It also includes security features to lock and unlock the system based on a predefined sequence of button presses.

Operating Instructions:
Setting Threshold:
To set the threshold for the waste level, enter a value between 0 and 100 in the provided entry field.
Click the "Set Threshold" button to apply the new threshold. The system will display the updated threshold value on the interface.
Security System:
The system starts in a locked state. To unlock the system, you need to enter a specific button sequence: Blue Button -> Red Button -> Blue Button.
Press the buttons in this sequence to unlock the system. When the correct sequence is entered, the green LED will light up, indicating that the system is unlocked.
If an incorrect sequence is entered, the red LED will light up briefly, indicating an unsuccessful attempt.
Monitoring Trash Level:
The system continuously monitors the trash level using the ultrasonic sensor.
The trash level percentage is displayed on the main interface. If the trash level exceeds the set threshold, the displayed percentage will turn red, indicating that the bin is approaching full capacity.
Lid Detection (Alarm):
The system also includes a lid detection feature using the ultrasonic sensor.
If the lid of the waste container is opened (distance > 6.0 cm), an alarm (buzzer) will be activated.
When the lid is closed, the alarm will deactivate.
Exiting the Application:
To exit the application and clean up the GPIO settings, click the "Exit" button.
This will safely exit the program and release all resources used by the Smart Waste Management System.
Important Notes:
Calibration: Ensure that the empty_distance and full_distance variables are calibrated according to your specific waste container setup.
Button Sequence: Modify the correct_sequence list in the security_system function if you wish to change the unlock sequence.
Polling Intervals: Adjust the polling intervals in the relevant functions (update_gui, check_lid) based on your specific requirements.
Please refer to this user manual for guidance on operating the Smart Waste Management System. If you have any questions or encounter issues, feel free to consult the system documentation or contact technical support for assistance. Thank you for using our system!