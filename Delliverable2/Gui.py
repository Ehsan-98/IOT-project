import tkinter as tk
from tkinter import ttk

def main_window():
    # Create main window
    root = tk.Tk()
    root.title("Smart Waste Management System")

    # Configure window size and position
    root.geometry("400x300")
    root.resizable(False, False)

    # Function to update waste threshold
    def set_threshold():
        new_threshold = entry_threshold.get()
        label_waste_level.config(text=f"Threshold set to {new_threshold}%")

    # Create a label to display waste level information
    label_waste_level = ttk.Label(root, text="Current Waste Level: 50%")
    label_waste_level.pack(pady=20)

    # Create an entry field to set the waste threshold
    entry_threshold = ttk.Entry(root, width=10)
    entry_threshold.insert(0, "80")  # Default threshold value
    entry_threshold.pack(pady=10)

    # Create a button to update the threshold
    button_set_threshold = ttk.Button(root, text="Set Threshold", command=set_threshold)
    button_set_threshold.pack(pady=10)

    # Start the main event loop
    root.mainloop()

# Run the main_window function when the script is executed
if __name__ == "__main__":
    main_window()

