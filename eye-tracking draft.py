import cv2
from scipy.spatial import distance as dist
from collections import deque
import numpy as np

# Keep last N eye positions for smoothing
eye_buffer = deque(maxlen=5)

# Load the eye cascade classifier
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Initialize video capture
cap = cv2.VideoCapture("example 2.mov")  # Use 0 for webcam


def calculate_ear(eye):
    # Calculate the Eye Aspect Ratio (EAR)
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear


def track_pupil(eye_frame):
    # Track the pupil by finding contours in the eye area
    gray = cv2.cvtColor(eye_frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)

    # Binary thresholding: pupils are dark so invert the binary mask
    _, thresh = cv2.threshold(blurred, 30, 255, cv2.THRESH_BINARY_INV)

    # Find all contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return None

    # Find the largest contour by area
    max_contour = max(contours, key=cv2.contourArea)
    max_area = cv2.contourArea(max_contour)

    # Filter: ignore if area is too small or too large (noise)
    h, w = eye_frame.shape[:2]
    frame_area = w * h
    if max_area < frame_area * 0.01 or max_area > frame_area * 0.5:
        return None  # too small or too large to be the pupil

    # Compute center of the contour
    M = cv2.moments(max_contour)
    if M["m00"] == 0:
        return None

    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])

    # Draw dot on pupil center
    cv2.circle(eye_frame, (cx, cy), 3, (255, 0, 0), -1)

    return (cx, cy)


while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)

    if len(eyes) > 0:
        # Get the largest eye
        largest_eye = max(eyes, key=lambda e: e[2] * e[3])
        eye_buffer.append(largest_eye)

        # Average the positions from the buffer for stability
        avg_eye = np.mean(eye_buffer, axis=0).astype(int)
        ex, ey, ew, eh = avg_eye

        # Compute center for EAR (unchanged)
        center_x = ex + ew // 2
        center_y = ey + eh // 2

        # EAR landmarks (fake points for demonstration)
        eye_landmarks = [
            (ex, ey + eh // 2),
            (ex + ew // 3, ey),
            (ex + 2 * ew // 3, ey),
            (ex + ew, ey + eh // 2),
            (ex + 2 * ew // 3, ey + eh),
            (ex + ew // 3, ey + eh)
        ]
        ear = calculate_ear(eye_landmarks)
        print(f'EAR: {ear:.2f}')

        # Check if the eye is closed based on EAR (EAR < 0.2 is considered closed)
        if ear < 0.2:
            cv2.putText(frame, "Eye is closed", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            print("Eye is closed")
            # Skip further processing if the eye is closed
            continue

        # Track the pupil in the detected eye region
        eye_frame = frame[ey:ey + eh, ex:ex + ew]
        pupil_center = track_pupil(eye_frame)

        if pupil_center:
            pcx, pcy = pupil_center
            offset_x = pcx - center_x
            offset_y = pcy - center_y

            cv2.circle(eye_frame, (pcx, pcy), 4, (255, 0, 0), -1)
            cv2.putText(eye_frame, f"Pupil: ({pcx}, {pcy})", (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255),
                        1)
            cv2.putText(eye_frame, f"Offset: ({offset_x}, {offset_y})", (5, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                        (0, 255, 255), 1)

        # Show the cropped eye frame with pupil detection
        cv2.imshow('Tracked Eye Only', eye_frame)

    # # Show the full frame with the "Eye is closed" message
    # cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()

