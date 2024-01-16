import numpy as np
import cv2
import json
from pyzbar import pyzbar
import datetime
import time

# Function to load user data from the JSON file
def load_user_data(filename):
    try:
        with open(filename, "r") as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = []
    return data

# Load existing user data from the "data.json" file
user_data = load_user_data("data.json")

# Dictionary to store active user sessions with last action time
active_sessions = {}

# File to store login and logout times
log_file = open("attendance_log.txt", "a")

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Set the delay time (in seconds) between logins and logouts
delay_time = 10

while True:
    success, img = cap.read()
    mycolor = (0, 0, 255)  # Default color for "Authentication failed"
    
    for barcode in pyzbar.decode(img):
        scanned_data = barcode.data.decode('utf-8')
        
        # Check if the scanned ID exists in user data
        user_found = False
        for user in user_data:
            if user['id'] == scanned_data:
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Check if the user is already in an active session
                if scanned_data in active_sessions:
                    last_action_time = active_sessions[scanned_data]

                    # Check if enough time has passed since the last action
                    if (datetime.datetime.now() - last_action_time).seconds >= delay_time:
                        # User is logging out
                        print(user['name'], "logged out at", current_time)
                        log_file.write(f"{user['name']} logged out at {current_time}\n")
                        active_sessions[scanned_data] = datetime.datetime.now()  # Update last action time
                    else:
                        print("Action too soon. Please wait.")
                else:
                    # User is logging in
                    print(user['name'], "logged in at", current_time)
                    log_file.write(f"{user['name']} logged in at {current_time}\n")
                    active_sessions[scanned_data] = datetime.datetime.now()
                    mycolor = (0, 255, 0)  # Change color to green for "Authentication Success"

                user_found = True
                break

        if not user_found:
            print("Authentication failed")

        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape(-1, 1, 2)
        cv2.polylines(img, [pts], True, mycolor, 5)
        pts2 = barcode.rect
        cv2.putText(img, "Authentication Success", (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, mycolor, 2)

    cv2.imshow("Result", img)
    cv2.waitKey(1)

# Release the camera and close the log file before exiting
cap.release()
log_file.close()
