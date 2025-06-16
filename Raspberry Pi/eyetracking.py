from picamera2 import Picamera2
import cv2
from collections import deque
import numpy as np
import time

# Initialize a deque to store the last N eye positions for smoothing
eye_buffer = deque(maxlen=5)

# Load the pre-trained Haar Cascade classifier for eye detection
eye_cascade = cv2.CascadeClassifier('/usr/share/opencv4/haarcascades/haarcascade_eye.xml')

# Initialize Picamera2
picam2 = Picamera2()
picam2.start()

def fit_circle_to_partial_pupil(contour):
    pts = contour.reshape(-1, 2)
    (x, y), radius = cv2.minEnclosingCircle(pts)
    center = (int(x), int(y))
    return center, int(radius)

def estimate_eye_closed(eye_frame):
    gray = cv2.cvtColor(eye_frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    black_pixels = np.sum(thresh == 0)
    total_pixels = thresh.size
    darkness_ratio = black_pixels / total_pixels
    return darkness_ratio > 0.7

def track_pupil(eye_frame, initial_threshold=30):
    gray = cv2.cvtColor(eye_frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)

    h, w = eye_frame.shape[:2]
    frame_area = w * h

    best_pupil = None
    best_thresh = initial_threshold
    step = 5
    max_attempts = 10

    thresholds = []
    for i in range(max_attempts):
        up = initial_threshold + step * i
        down = initial_threshold - step * i
        if up <= 255:
            thresholds.append(up)
        if down >= 0 and down != up:
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
                    (x, y), radius = cv2.minEnclosingCircle(max_contour)
                    if radius > 1:
                        best_pupil = (int(x), int(y))
                        best_thresh = threshold
                        break

    if best_pupil:
        cv2.circle(eye_frame, best_pupil, 3, (255, 0, 0), -1)

    return best_pupil

def median_smooth_position(eye_buffer):
    if len(eye_buffer) > 1:
        smoothed_position = np.median(np.array(eye_buffer), axis=0).astype(int)
        return smoothed_position
    return eye_buffer[-1]

def main():
    eye_bbox_fixed = None
    last_update_time = 0

    while True:
        frame = picam2.capture_array()  # 获取 NumPy 格式的当前帧

        current_time = time.time()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 每300秒更新一次眼睛检测区域
        if current_time - last_update_time > 600:
            eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)
            if len(eyes) > 0:
                eye_bbox_fixed = max(eyes, key=lambda e: e[2] * e[3])
                last_update_time = current_time

        if eye_bbox_fixed is not None:
            ex, ey, ew, eh = eye_bbox_fixed

            crop_w, crop_h = ew, eh
            center_x = ex + ew // 2
            center_y = ey + eh // 2

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
                rel_x = 1 - pcx / (crop_x2 - crop_x1)
                rel_y = 1 - pcy / (crop_y2 - crop_y1)
                yield rel_x, rel_y

        if cv2.waitKey(1) & 0xFF == 27:
            break

if __name__ == '__main__':
    try:
        for rel_x, rel_y in main():
            print(f"Pupil position (relative): x={rel_x:.2f}, y={rel_y:.2f}")
    finally:
        picam2.stop()
        cv2.destroyAllWindows()
