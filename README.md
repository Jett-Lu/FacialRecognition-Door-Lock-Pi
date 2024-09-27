Smart Facial Recognition-Based Door Lock
Overview

The IntelliGuard project integrates advanced facial recognition technology with a Raspberry Pi 4 to create a secure and user-friendly access control system. It leverages real-time video processing, event logging, and push notifications to enhance security and user experience.
Components

-Camera: Captures live footage for real-time facial comparison.
-Raspberry Pi 4: Central processing unit that runs the system.
-LEDs: Indicate lock status (red for denied, green for granted).
-Buzzer: Provides audio feedback upon successful access.
-LCD Display: Shows messages and prompts to users.
-Push Notifications: Alerts authorized personnel about access events.

Features

-User Authentication: Uses facial recognition to grant or deny access.
-Event Logging: Records access attempts in a CSV file with timestamps.
-Real-Time Feedback: Provides visual and audio cues during user interactions.

Setup Instructions

1. Initial Setup:
    -Ensure all components are intact.
    -Add authorized users to the dataset.
    -Configure the .env file with your PushBullet access token.

2. User Authentication:
    -Run app.py to initiate the system.
    -Access the system through the provided URL on the same network.
    -Follow LCD prompts for user interactions.

Maintenance

-Regularly update software libraries and the Raspberry Pi OS.
-Review and optimize the facial recognition database.
-Conduct routine inspections of hardware components.

Future Developments

-Improve facial recognition algorithms with machine learning.
-Enhance system scalability and compatibility.
-Explore integration with smart home ecosystems.

Bill of Materials

-USB Cam
-Raspberry Pi 4 Model B
-RGB LEDs
-Buzzer Piezo
-LCD1602 I2C Display
