import cv2
from collections import deque
import numpy as np
import math
import time
# Initialize a deque to store the last N eye positions for smoothing
eye_buffer = deque(maxlen=5)

# Load the pre-trained Haar Cascade classifier for eye detection
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Initialize video capture
cap = cv2.VideoCapture(0)  # Use 0 for webcam

def classify_point(x, y):
    a = 0.75
    cx, cy = 0.5, 0.5

    r1 = 0.15*a  # inner circle
    r2 = 0.3*a   # outer circle
    
    # distance from center
    dist = math.hypot(x - cx, y - cy)

    if dist <= r1:
        region_type = "inner circle"
    elif dist <= r2:
        region_type = "outer circle"
    else:
        region_type = "outside"

    if x < cx and y > cy:
        quadrant = "top-left"
    elif x > cx and y > cy:
        quadrant = "top-right"
    elif x < cx and y < cy:
        quadrant = "bottom-left"
    elif x > cx and y < cy:
        quadrant = "bottom-right"
    elif x == cx and y == cy:
        quadrant = "center"
    elif x == cx:
        quadrant = "vertical line"
    elif y == cy:
        quadrant = "horizontal line"
    else:
        quadrant = "unknown"
    if region_type == "outside" and quadrant == "top-left":
        region = "A"
    elif region_type == "outside" and quadrant == "top-right":
        region = "B"
    elif region_type == "outside" and quadrant == "bottom-left":
        region = "C"
    elif region_type == "outside" and quadrant == "bottom-right":
        region = "D"
    elif region_type == "outer circle" and quadrant == "top-left":
        region = "E"
    elif region_type == "outer circle" and quadrant == "top-right":
        region = "F"
    elif region_type == "outer circle" and quadrant == "bottom-left":
        region = "G"
    elif region_type == "outer circle" and quadrant == "bottom-right":
        region = "H"
    elif region_type == "inner circle" and quadrant == "top-left":
        region = "I"
    elif region_type == "inner circle" and quadrant == "top-right":
        region = "J"
    elif region_type == "inner circle" and quadrant == "bottom-left":
        region = "K"
    elif region_type == "inner circle" and quadrant == "bottom-right":
        region = "L"
    else:
        region = "not detected"
    return region,(x - cx, y - cy)

def estimate_eye_closed(eye_frame):
    """Estimate if the eye is closed based on the darkness ratio."""
    gray = cv2.cvtColor(eye_frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 50, 255, cv2.THRESH_BINARY)

    black_pixels = np.sum(thresh == 0)
    total_pixels = thresh.size
    darkness_ratio = black_pixels / total_pixels

    return darkness_ratio > 0.6  # Adjust this threshold as needed

def track_pupil(eye_frame, initial_threshold=30):
    gray = cv2.cvtColor(eye_frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)

    h, w = eye_frame.shape[:2]
    frame_area = w * h

    best_pupil = None
    best_thresh = initial_threshold
    threshold = initial_threshold
    step = 5  # how much to increment/decrement threshold
    max_attempts = 10

    for i in range(max_attempts):
        _, thresh_img = cv2.threshold(blurred, threshold, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            max_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(max_contour)

            # Validate area
            if frame_area * 0.01 < area < frame_area * 0.5: #If detected pupil is too large or too small
                M = cv2.moments(max_contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    best_pupil = (cx, cy)
                    best_thresh = threshold
                    break
                else:
                    threshold += step  # try a different threshold
            else:
                threshold += step  # area too small/large
        else:
            threshold += step  # no contour found

        if threshold > 255:
            threshold = 255
            break

    if best_pupil:
        cv2.circle(eye_frame, best_pupil, 3, (255, 0, 0), -1)
        # Optional: display threshold used
        cv2.putText(eye_frame, f"Thresh: {best_thresh}", (5, 55), cv2.FONT_HERSHEY_SIMPLEX,
                    0.45, (0, 255, 0), 1)

    return best_pupil


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
            # print("Eye is closed")
            cv2.imshow("Frame", frame)
            #if cv2.waitKey(1) & 0xFF == 27:
                #break
            #continue

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
            region, offset = classify_point(rel_x, rel_y)

            # ✅ 输出到终端
            print(f"Region: {region}, relative coordinate: {rel_x, rel_y}")
    time.sleep(0.5)
            # ✅ 或显示到图像上
            # cv2.putText(eye_frame, f"Region: {region}", (5, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.45,
            #     (0, 255, 0), 1)
            # # Draw normalized position as text
            # cv2.putText(eye_frame, f"Norm: ({rel_x:.2f}, {rel_y:.2f})", (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45,
            #             (255, 255, 255), 1)
            # cv2.putText(eye_frame, f"Offset: ({offset_x}, {offset_y})", (5, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.45,
            #             (0, 255, 255), 1)


        # Show cropped eye frame
        # cv2.imshow('Tracked Eye Only', eye_frame)

    #if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        #break

cap.release()
cv2.destroyAllWindows()




