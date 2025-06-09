import json
import os
import time
from eyetracking import main as gaze_stream
import math

CALIBRATION_FILE = "calibration_data.json"
corner_labels = ["center", "top_mid", "left_mid", "bottom_mid", "right_mid"]

def classify_point(x, y):
    a = 1
    cx, cy = 0.5, 0.5
    dx = x - cx
    dy = y - cy
    dist = math.hypot(dx, dy)

    inner_radius = 0.25 * a
    outer_radius = 0.47 * a

    if dist <= inner_radius:
        return "25"
    
    elif dist <= outer_radius:
        angle = math.degrees(math.atan2(dy, dx)) % 360
        if 0 <= angle < 36:
            return "1"
        elif 36 <= angle < 45:
            return "2"
        elif 45 <= angle < 360/7:
            return "3"
        elif 360/7 <= angle < 72:
            return "4"
        elif 72 <= angle < 2*360/7:
            return "5"
        elif 2*360/7 <= angle < 108:
            return "6"
        elif 108 <= angle < 135:
            return "7"
        elif 135 <= angle < 144:
            return "8"
        elif 144 <= angle < 3*360/7:
            return "9"
        elif 3*360/7 <= angle < 180:
            return "10"
        elif 180 <= angle < 4*360/7:
            return "11"
        elif 4*360/7 <= angle < 216:
            return "12"
        elif 216 <= angle < 225:
            return "13"
        elif 225 <= angle < 252:
            return "14"
        elif 252 <= angle < 5*360/7:
            return "15"
        elif 5*360/7 <= angle < 288:
            return "16"
        elif 288 <= angle < 6*360/7:
            return "17"
        elif 6*360/7 <= angle < 315:
            return "18"
        elif 315 <= angle < 324:
            return "19"
        else:
            return "20"
    else:
        if x < 0.5 and y < 0.5:
            return "23"
        elif x > 0.5 and y < 0.5:
            return "24"
        elif x < 0.5 and y > 0.5:
            return "21"
        elif x > 0.5 and y > 0.5:
            return "22"
        else:
            return "outside"

class Calibration:
    def __init__(self):
        self.corners = {}
        if os.path.exists(CALIBRATION_FILE):
            with open(CALIBRATION_FILE, 'r') as f:
                self.corners = json.load(f)

    def calibrate(self, gaze_generator):
        self.corners = {}
        for label in corner_labels:
            print(f"\nLook at the {label.replace('_', ' ')}...")
            for i in range(3, 0, -1):
                print(f"Capturing in {i}...", end="\r")
                time.sleep(1)
            rel_x, rel_y = next(gaze_generator)
            self.corners[label] = {"x": rel_x, "y": rel_y}
            print(f"Recorded {label}: ({rel_x:.3f}, {rel_y:.3f})")
        with open(CALIBRATION_FILE, 'w') as f:
            json.dump(self.corners, f)
            print("[INFO] Calibration data saved.")

    def transform_coordinates(self, rel_x, rel_y):
        if len(self.corners) != 5:
            raise ValueError("Calibration data is incomplete. Please calibrate.")

        center = self.corners["center"]
        top_mid = self.corners["top_mid"]
        left_mid = self.corners["left_mid"]
        bottom_mid = self.corners["bottom_mid"]
        right_mid = self.corners["right_mid"]

        cx, cy = center["x"], center["y"]
        tx, ty = top_mid["x"], top_mid["y"]
        lx, ly = left_mid["x"], left_mid["y"]
        bx, by = bottom_mid["x"], bottom_mid["y"]
        rx, ry = right_mid["x"], right_mid["y"]

        dx = rel_x - cx
        dy = rel_y - cy

        if dx >= 0 and dy > 0:
            ref_x, ref_y = rx - cx, ty - cy
        elif dx < 0 and dy > 0:
            ref_x, ref_y = - (lx - cx), ty - cy
        elif dx < 0 and dy <= 0:
            ref_x, ref_y = - (lx - cx), - (by - cy)
        else:
            ref_x, ref_y = rx - cx, - (by - cy)

        norm_x = dx / ref_x if ref_x != 0 else 0.0
        norm_y = dy / ref_y if ref_y != 0 else 0.0

        calibrated_x = max(0.0, min(1.0, 0.5 + norm_x / 2))
        calibrated_y = max(0.0, min(1.0, 0.5 + norm_y / 2))

        return calibrated_x, calibrated_y

if __name__ == "__main__":
    stream = gaze_stream()
    calib_file = "calibration_data.json"

    if os.path.exists(calib_file):
        with open(calib_file, 'r') as f:
            try:
                data = json.load(f)
                if data:
                    os.remove(calib_file)
            except json.JSONDecodeError:
                print("[WARNING] Calibration file exists but is invalid. Recreating it.")
                os.remove(calib_file)

    calib = Calibration()
    calib.calibrate(stream)

    with open(calib_file, 'w') as f:
        json.dump(calib.corners, f)
        print("[INFO] New calibration data saved.")

    print("\n[INFO] Starting live gaze processing (press Ctrl+C to stop):")
    try:
        for rel_x, rel_y in stream:
            cal_x, cal_y = calib.transform_coordinates(rel_x, rel_y)
            region = classify_point(cal_x, cal_y)
            print(region)
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n[INFO] Gaze processing stopped.")
