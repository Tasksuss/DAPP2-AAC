import cv2
from collections import deque
import numpy as np

# Initialize a deque to store the last N eye positions for smoothing
eye_buffer = deque(maxlen=5)

# Load the pre-trained Haar Cascade classifier for eye detection
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Initialize video capture
cap = cv2.VideoCapture("example 2.mov")  # Use 0 for webcam

def estimate_eye_closed(eye_frame):
    """Estimate if the eye is closed based on the darkness ratio."""
    gray = cv2.cvtColor(eye_frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 50, 255, cv2.THRESH_BINARY)

    black_pixels = np.sum(thresh == 0)
    total_pixels = thresh.size
    darkness_ratio = black_pixels / total_pixels

    return darkness_ratio > 0.6  # Adjust this threshold as needed

def track_pupil(eye_frame):
    """Track the pupil's position within the eye frame."""
    gray = cv2.cvtColor(eye_frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    _, thresh = cv2.threshold(blurred, 30, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None

    max_contour = max(contours, key=cv2.contourArea)
    max_area = cv2.contourArea(max_contour)

    h, w = eye_frame.shape[:2]
    frame_area = w * h
    if max_area < frame_area * 0.01 or max_area > frame_area * 0.5:
        return None

    M = cv2.moments(max_contour)
    if M["m00"] == 0:
        return None

    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])

    cv2.circle(eye_frame, (cx, cy), 3, (255, 0, 0), -1)

    return (cx, cy)

def median_smooth_position(eye_buffer):
    """Smooth the eye position using median filtering on the last N frames."""
    if len(eye_buffer) > 1:
        smoothed_position = np.median(np.array(eye_buffer), axis=0).astype(int)
        return smoothed_position
    return eye_buffer[-1]

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)

    if len(eyes) > 0:
        largest_eye = max(eyes, key=lambda e: e[2] * e[3])
        eye_buffer.append(largest_eye)

        # Apply median smoothing to the eye position
        avg_eye = median_smooth_position(eye_buffer)
        ex, ey, ew, eh = avg_eye

        # Define crop size around center of the eye
        crop_w, crop_h = ew, eh
        center_x = ex + ew // 2
        center_y = ey + eh // 2

        # Calculate crop region around eye center
        crop_x1 = max(center_x - crop_w // 2, 0)
        crop_y1 = max(center_y - crop_h // 2, 0)
        crop_x2 = min(crop_x1 + crop_w, frame.shape[1])
        crop_y2 = min(crop_y1 + crop_h, frame.shape[0])

        eye_frame = frame[crop_y1:crop_y2, crop_x1:crop_x2].copy()

        if estimate_eye_closed(eye_frame):
            cv2.putText(frame, "Eye is closed", (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 2)
            print("Eye is closed")
            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break
            continue

        # Pupil tracking
        pupil_center = track_pupil(eye_frame)
        if pupil_center:
            pcx, pcy = pupil_center
            center_x = ew // 2
            center_y = eh // 2
            offset_x = pcx - center_x
            offset_y = pcy - center_y

            cv2.circle(eye_frame, (pcx, pcy), 4, (255, 0, 0), -1)
            # Normalize pupil position to [0, 1] based on cropped area size
            rel_x = pcx / (crop_x2 - crop_x1)
            rel_y = pcy / (crop_y2 - crop_y1)

            # Draw normalized position as text
            cv2.putText(eye_frame, f"Norm: ({rel_x:.2f}, {rel_y:.2f})", (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                        (255, 255, 255), 1)
            cv2.putText(eye_frame, f"Offset: ({offset_x}, {offset_y})", (5, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                        (0, 255, 255), 1)

        # Show cropped eye frame
        cv2.imshow('Tracked Eye Only', eye_frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
