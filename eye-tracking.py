import cv2
import pyautogui
import numpy as np

# Initialize video capture and screen dimensions
cap = cv2.VideoCapture(0)
screen_w, screen_h = pyautogui.size()

# Load Haar cascades for face and eye detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Configuration parameters
SMOOTHING_FACTOR = 0.5  # Between 0 and 1 (higher = smoother)
MOVEMENT_SCALE = 2.5  # Adjust sensitivity of eye movement to mouse movement

# Initialize variables for smoothing
screen_x, screen_y = pyautogui.position()
prev_eyes = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip frame horizontally and convert to grayscale
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        # Extract face ROI
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        # Detect eyes within face region
        eyes = eye_cascade.detectMultiScale(roi_gray)

        if len(eyes) >= 2:
            # Sort eyes by x-coordinate and take first two
            eyes = sorted(eyes, key=lambda x: x[0])[:2]
            current_eyes = []

            for (ex, ey, ew, eh) in eyes:
                # Calculate eye centers relative to full frame
                eye_center = (x + ex + ew // 2, y + ey + eh // 2)
                current_eyes.append(eye_center)

                # Draw eye markers (optional)
                cv2.circle(frame, eye_center, 5, (0, 255, 0), -1)

            if prev_eyes:
                # Calculate average movement between frames
                delta_x = (current_eyes[0][0] + current_eyes[1][0] -
                           prev_eyes[0][0] - prev_eyes[1][0]) / 2
                delta_y = (current_eyes[0][1] + current_eyes[1][1] -
                           prev_eyes[0][1] - prev_eyes[1][1]) / 2

                # Scale deltas to screen dimensions
                delta_x = delta_x * (screen_w / frame.shape[1]) * MOVEMENT_SCALE
                delta_y = delta_y * (screen_h / frame.shape[0]) * MOVEMENT_SCALE

                # Apply smoothing
                screen_x = screen_x * SMOOTHING_FACTOR + (screen_x + delta_x) * (1 - SMOOTHING_FACTOR)
                screen_y = screen_y * SMOOTHING_FACTOR + (screen_y + delta_y) * (1 - SMOOTHING_FACTOR)

                # Keep cursor within screen bounds
                screen_x = max(0, min(screen_w, screen_x))
                screen_y = max(0, min(screen_h, screen_y))

                # Move mouse
                pyautogui.moveTo(screen_x, screen_y)

            prev_eyes = current_eyes

    # Display frame (optional)
    cv2.imshow('Eye Tracking', frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
