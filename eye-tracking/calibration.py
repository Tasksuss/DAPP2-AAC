# calibration.py
import json
import os
from eyetracking import main as gaze_stream
import math

CALIBRATION_FILE = "calibration_data.json"
corner_labels = ["top_left", "top_right", "bottom_left", "bottom_right"]

def classify_point(x, y):
    a = 0.75
    cx, cy = 0.5, 0.5
    dx = x - cx
    dy = y - cy
    dist = math.hypot(dx, dy)

    inner_radius = 0.2*a    # inner circle
    outer_radius = 0.35*a     # middle circle

    # comfirm whether in inner circle
    if dist <= inner_radius:
        return "inner circle"

    # comfirm whether in outer circle
    elif dist <= outer_radius:
        angle = math.degrees(math.atan2(-dy, dx)) % 360  # clockwise from right
        if 45 <= angle < 135:
            return "top ring"      # h l d r n t s
        elif 135 <= angle < 225:
            return "left ring"     # c w m g y p f
        elif 225 <= angle < 315:
            return "bottom ring"   # j b q k v z x
        else:
            return "right ring"    # u o i e a

    # outer circle
    else:
        if x < 0.5 and y < 0.5:
            return "bottom-left (X)"
        elif x > 0.5 and y < 0.5:
            return "bottom-right (✓)"
        elif x < 0.5 and y > 0.5:
            return "top-left (NUM)"
        elif x > 0.5 and y > 0.5:
            return "top-right (⟳)"
        else:
            return "outside"

class Calibration:
    def __init__(self):
        self.corners = {}
        if os.path.exists(CALIBRATION_FILE):
            with open(CALIBRATION_FILE, 'r') as f:
                self.corners = json.load(f)
                print("[INFO] Loaded calibration data.")
        else:
            print("[INFO] No calibration data found. Please run calibration.")

    def calibrate(self, gaze_generator):
        print("Calibration: Look at the prompted corner and press ENTER to capture gaze.")
        self.corners = {}

        for label in corner_labels:
            input(f"\nLook at the {label.replace('_', ' ')} and press ENTER...")
            rel_x, rel_y = next(gaze_generator)
            self.corners[label] = {"x": rel_x, "y": rel_y}
            print(f"Recorded {label}: ({rel_x:.3f}, {rel_y:.3f})")

        with open(CALIBRATION_FILE, 'w') as f:
            json.dump(self.corners, f)
            print("[INFO] Calibration data saved.")

    def transform_coordinates(self, rel_x, rel_y):
        if len(self.corners) != 4:
            raise ValueError("Calibration data is incomplete. Please calibrate.")

        tl = self.corners["top_left"]
        tr = self.corners["top_right"]
        bl = self.corners["bottom_left"]
        br = self.corners["bottom_right"]

        min_x = (tl["x"] + bl["x"]) / 2
        max_x = (tr["x"] + br["x"]) / 2
        min_y = (tl["y"] + tr["y"]) / 2
        max_y = (bl["y"] + br["y"]) / 2

        calibrated_x = (rel_x - min_x) / (max_x - min_x)
        calibrated_y = 1 - (rel_y - min_y) / (max_y - min_y)

        # Clamp values
        calibrated_x = max(0.0, min(1.0, calibrated_x))
        calibrated_y = max(0.0, min(1.0, calibrated_y))

        return calibrated_x, calibrated_y


# === MAIN USE ===
if __name__ == "__main__":
    stream = gaze_stream()
    calib_file = "calibration_data.json"

    # Check if file exists and has data
    if os.path.exists(calib_file):
        with open(calib_file, 'r') as f:
            try:
                data = json.load(f)
                if data:
                    print("[INFO] Existing calibration data found. Deleting it...")
                    os.remove(calib_file)
            except json.JSONDecodeError:
                print("[WARNING] Calibration file exists but is invalid. Recreating it.")
                os.remove(calib_file)

    # Create a new Calibration instance (which loads fresh or empty)
    calib = Calibration()

    print("[INFO] Running calibration...")
    calib.calibrate(stream)

    # Save the new calibration data
    with open(calib_file, 'w') as f:
        json.dump(calib.corners, f)
        print("[INFO] New calibration data saved.")

    # Start live tracking
    print("\n[INFO] Starting live gaze processing (press Ctrl+C to stop):")
    try:
        for rel_x, rel_y in stream:
            cal_x, cal_y = calib.transform_coordinates(rel_x, rel_y)
            region = classify_point(cal_x, cal_y)
            print(region)
    except KeyboardInterrupt:
        print("\n[INFO] Gaze processing stopped.")


