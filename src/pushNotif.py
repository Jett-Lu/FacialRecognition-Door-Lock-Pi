from pushbullet import Pushbullet
from dotenv import load_dotenv
import os
import datetime

load_dotenv()
pushbullet_api_key = os.getenv("PUSHBULLET_API_KEY")
pb = Pushbullet(pushbullet_api_key)

# Initialize a variable to store the last time a notification was sent
last_notification_time = None

# Define the cooldown period (in seconds)
cooldown_period = 25  # Adjust as needed

def send_notification(detected_name):
    global last_notification_time

    # Get the current time
    current_time = datetime.datetime.now()

    # Check if enough time has elapsed since the last notification
    if last_notification_time is None or (current_time - last_notification_time).total_seconds() >= cooldown_period:
        # Update the last notification time
        last_notification_time = current_time

        # Construct the notification message
        current_day = current_time.strftime("%A")
        if detected_name == "Unknown":
            title = "Unknown Person Detected"
            message = f"Unknown person detected at {current_time.strftime('%H:%M:%S')} on {current_day}."
        else:
            title = "Person Detected"
            message = f"{detected_name} detected at {current_time.strftime('%H:%M:%S')} on {current_day}."

        # Send the notification
        pb.push_note(title, message)
