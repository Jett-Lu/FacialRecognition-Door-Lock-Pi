import signal
import time
from flask import Flask, render_template, Response
import cv2
import face_recognition
import os
from pushNotif import send_notification
from eventLogger import log_event
from rpi_lcd import LCD
from gpiozero import RGBLED, PWMOutputDevice
from datetime import datetime
from time import sleep
from bootSequence import startup_sequence
from exitSequence import exit_handler

# Global variables

app = Flask(__name__, template_folder='../templates')

# Load known faces and their encodings
known_face_encodings = []
known_face_names = []

# Path to the dataset directory
dataset_path = '../dataSet'

# Initialize the LCD display
lcd = LCD()

# Initialize LED
led = RGBLED(red=26, green=19, blue=13)

# Control variables for frame rate limitation
frame_interval = 10  # Number of frames to skip
frame_count = 0

# Initialize the video capture device
video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Set width
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Set height

# Define the GPIO pin connected to the buzzer
buzzer_pin = 20  # Change this to match the GPIO pin you're using

# Initialize the PWMOutputDevice for the buzzer
buzzer = PWMOutputDevice(buzzer_pin)

# Define a cooldown duration in seconds
cooldown_duration = 10  # 10 seconds cooldown

# Initialize last_known_person_detected_time
last_known_person_detected_time = datetime.min

def signal_handler(sig, frame):
    exit_handler(video_capture, led, lcd)

# Function to load and encode faces from the dataset
def load_and_encode_faces(dataset_path):
    known_face_encodings = []
    known_face_names = []

    # Iterate over the folders in dataset
    for name in os.listdir(dataset_path):
        person_path = os.path.join(dataset_path, name)
        if os.path.isdir(person_path):
            # Iterate over each image in the person's folder
            for image_filename in os.listdir(person_path):
                image_path = os.path.join(person_path, image_filename)
                image = face_recognition.load_image_file(image_path)
                encoding = face_recognition.face_encodings(image)
                if encoding:
                    known_face_encodings.append(encoding[0])
                    known_face_names.append(name)

    return known_face_encodings, known_face_names

# Load known faces and their encodings
known_face_encodings, known_face_names = load_and_encode_faces(dataset_path)

def handle_led_color(known_face_detected, unknown_face_detected):
    if known_face_detected:
        # Known face detected, LED is green
        led.color = (0, 0.3, 0)
    elif unknown_face_detected:
        # Unknown face detected, LED is red
        led.color = (0.3, 0, 0)
    else:
        # Nobody detected, flash blue
        led.color = (0, 0, 1)  # Blue
        sleep(0.5)  # Flash duration
        led.off()  # Turn off the LED

def buzz_buzzer():
    # Loop the buzzer twice
    for _ in range(2):
        buzzer.value = 6 / 10.0  # Convert to duty cycle (0.0 to 1.0)
        sleep(0.2)        # Keep the buzzer on for 0.2 seconds

        buzzer.off()  # Turn the buzzer off
        sleep(0.2)        # Wait for 0.2 seconds before next iteration
    
    buzzer.value = 6 / 10.0  # Convert to duty cycle (0.0 to 1.0)
    sleep(0.5)
    buzzer.off()

def generate_frames():
    global frame_count
    global last_known_person_detected_time

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        frame_count += 1

        # Skip frames if needed to limit frame rate
        if frame_count % frame_interval != 0:
            continue

        if not ret:
            break

        # Convert the frame from BGR to RGB
        rgb_frame = frame[:, :, ::-1]

        # Detect faces in the frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Initialize variables to track known and unknown faces
        known_face_detected = False
        unknown_face_detected = False
        known_face_name = None

        # Loop over each detected face
        for face_location, face_encoding in zip(face_locations, face_encodings):
            # Compare each face found in the frame to known faces
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # Check if any face matches with known faces
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                known_face_detected = True
                known_face_name = name
            else:
                unknown_face_detected = True

            # Draw a box around the face
            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            # Add text label with high contrast
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)  # Black border
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)  # White text

        # Handle LED color based on face detection
        handle_led_color(known_face_detected, unknown_face_detected)

        # Display the detected person's name on the LCD
        if known_face_detected:
            lcd.clear()
            lcd.text("Welcome", 1)
            lcd.text(known_face_name, 2)
        elif unknown_face_detected:
            lcd.clear()
            lcd.text("Unknown person", 1)
            lcd.text("Contact Admin", 2)
        else:
            lcd.clear()
            lcd.text("Please face the", 1)
            lcd.text("camera to begin", 2)

        # Log event and send notification for detected known faces
        if known_face_detected:
            # Check if cooldown period has passed
            current_time = datetime.now()
            if (current_time - last_known_person_detected_time).total_seconds() >= cooldown_duration:
                # Perform actions only if cooldown period has passed
                log_event(known_face_name)
                send_notification(known_face_name)
                last_known_person_detected_time = current_time  # Update last detected time

                # Buzz the buzzer
                buzz_buzzer()

        # If only unknown face detected, push to Pushbullet and log
        if unknown_face_detected and not known_face_detected:
            log_event("Unknown")
            send_notification("Unknown")

        # Encode the frame in JPEG format
        success, buffer = cv2.imencode('.jpg', frame)
        if success:
            yield (b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. The route that will stream the video."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    startup_sequence(led, lcd)
    signal.signal(signal.SIGINT, signal_handler)  # Register signal handler for Ctrl+C
    app.run(debug=False, host='0.0.0.0')
