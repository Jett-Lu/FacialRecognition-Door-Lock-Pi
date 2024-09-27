import csv
import datetime
import time  # Import the time module

# CSV file path
CSV_FILE = '../eventLogs.csv'

# Initialize a variable to store the last time an event was logged
last_log_time = None

# Define the cooldown period (in seconds)
cooldown_period = 25  # Adjust as needed

def log_event(name):
    """Logs an event with the given name and current date and time to the CSV file."""
    global last_log_time

    # Get the current time
    current_time = datetime.datetime.now()

    # Check if enough time has elapsed since the last event was logged
    if last_log_time is None or (current_time - last_log_time).total_seconds() >= cooldown_period:
        # Update the last log time
        last_log_time = current_time

        # Log the event to the CSV file
        current_day = current_time.strftime("%Y-%m-%d")
        current_time_str = current_time.strftime("%H:%M:%S")
        with open(CSV_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([current_day, current_time_str, name])
