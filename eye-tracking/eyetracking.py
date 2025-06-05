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


def fit_circle_to_partial_pupil(contour):
    # Convert contour to 2D point list
    pts = contour.reshape(-1, 2)

    # Fit a circle (least-squares)
    (x, y), radius = cv2.minEnclosingCircle(pts)
    center = (int(x), int(y))
    return center, int(radius)

def estimate_eye_closed(eye_frame):
    """Estimate if the eye is closed based on the darkness ratio."""
    gray = cv2.cvtColor(eye_frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)


    black_pixels = np.sum(thresh == 0)
    total_pixels = thresh.size
    darkness_ratio = black_pixels / total_pixels
    # cv2.imshow('filter', thresh)

    return darkness_ratio > 0.7  # Adjust this threshold as needed

def track_pupil(eye_frame, initial_threshold=30):
    gray = cv2.cvtColor(eye_frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)

    h, w = eye_frame.shape[:2]
    frame_area = w * h

    best_pupil = None
    best_thresh = initial_threshold
    step = 5
    max_attempts = 10

    # Build a threshold list that includes both increasing and decreasing values
    thresholds = []
    for i in range(max_attempts):
        up = initial_threshold + step * i
        down = initial_threshold - step * i
        if up <= 255:
            thresholds.append(up)
        if down >= 0 and down != up:  # Avoid duplicate threshold
            thresholds.append(down)

    for threshold in thresholds:
        _, thresh_img = cv2.threshold(blurred, threshold, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            max_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(max_contour)

            if frame_area * 0.01 < area < frame_area * 0.5:
                M = cv2.moments(max_contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    best_pupil = (cx, cy)
                    best_thresh = threshold
                    break
                else:
                    # Fallback to circle fitting if moments failed
                    (x, y), radius = cv2.minEnclosingCircle(max_contour)
                    if radius > 1:  # Avoid tiny noise
                        best_pupil = (int(x), int(y))
                        best_thresh = threshold
                        break

    if best_pupil:
        cv2.circle(eye_frame, best_pupil, 3, (255, 0, 0), -1)

    # cv2.imshow('gray', thresh_img)

    return best_pupil



def median_smooth_position(eye_buffer):
    """Smooth the eye position using median filtering on the last N frames."""
    if len(eye_buffer) > 1:
        smoothed_position = np.median(np.array(eye_buffer), axis=0).astype(int)
        return smoothed_position
    return eye_buffer[-1]

def main():
    eye_bbox_fixed = None
    last_update_time = 0  # Track last update time

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        current_time = time.time()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Update eye bbox every 5 seconds
        # if current_time - last_update_time > 30:
        eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)
        if len(eyes) > 0:
            eye_bbox_fixed = max(eyes, key=lambda e: e[2] * e[3])
            #     print(f"[INFO] Updated eye region: {eye_bbox_fixed}")
            #     last_update_time = current_time
            # else:
            #     print("[WARNING] No eyes detected on update attempt.")

        if eye_bbox_fixed is not None:
            ex, ey, ew, eh = eye_bbox_fixed

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

            pupil_center = track_pupil(eye_frame)

            if pupil_center is None and estimate_eye_closed(eye_frame):
                print("Eye is likely closed")
                continue

            if pupil_center:
                pcx, pcy = pupil_center
                center_x = ew // 2
                center_y = eh // 2
                rel_x = 1 - pcx / (crop_x2 - crop_x1)
                rel_y = 1 - pcy / (crop_y2 - crop_y1)
                yield rel_x, rel_y


                # print(rel_x, rel_y)
                # cv2.imshow('Tracked Eye Only', eye_frame)
                time.sleep(1)

        if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
            break



if __name__ == '__main__':
    main()
    cap.release()
    cv2.destroyAllWindows()
