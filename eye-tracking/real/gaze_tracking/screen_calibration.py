import numpy as np
import cv2
import json
from datetime import datetime


class ScreenCalibration:
    def __init__(self, screen_width=1920, screen_height=1080):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.calibration_points = []
        self.gaze_data = []
        self.transformation_matrix = None
        self.is_calibrated = False

    def add_calibration_point(self, screen_x, screen_y, left_pupil, right_pupil, horizontal_ratio, vertical_ratio):
        """Add a calibration data point"""
        self.calibration_points.append({
            'screen': (screen_x, screen_y),
            'left_pupil': left_pupil,
            'right_pupil': right_pupil,
            'horizontal_ratio': horizontal_ratio,
            'vertical_ratio': vertical_ratio
        })

    def calculate_transformation(self):
        """Calculate transformation matrix from gaze ratios to screen coordinates"""
        if len(self.calibration_points) < 4:  # Minimum 4 points needed
            return False

        # Extract features and targets
        features = []
        targets = []

        for point in self.calibration_points:
            # Simplified feature set for 5-point calibration
            feature = [
                1,  # bias term
                point['horizontal_ratio'],
                point['vertical_ratio'],
                point['horizontal_ratio'] ** 2,  # quadratic terms for better accuracy
                point['vertical_ratio'] ** 2,
                point['horizontal_ratio'] * point['vertical_ratio']  # interaction term
            ]
            features.append(feature)
            targets.append(point['screen'])

        features = np.array(features)
        targets = np.array(targets)

        # Use least squares regression
        try:
            self.transformation_matrix = np.linalg.lstsq(features, targets, rcond=None)[0]
            self.is_calibrated = True
            print(f"Calibration successful with {len(self.calibration_points)} points")
            return True
        except np.linalg.LinAlgError:
            print("Calibration failed: Could not solve transformation matrix")
            return False

    def predict_screen_position(self, horizontal_ratio, vertical_ratio, left_pupil, right_pupil):
        """Predict screen coordinates from gaze data"""
        if not self.is_calibrated or horizontal_ratio is None or vertical_ratio is None:
            return None

        feature = np.array([
            1,  # bias term
            horizontal_ratio,
            vertical_ratio,
            horizontal_ratio ** 2,
            vertical_ratio ** 2,
            horizontal_ratio * vertical_ratio
        ])

        screen_pos = feature.dot(self.transformation_matrix)

        # Clamp to screen bounds with some smoothing
        x = max(0, min(self.screen_width, screen_pos[0]))
        y = max(0, min(self.screen_height, screen_pos[1]))

        return (int(x), int(y))

    def save_calibration(self, filename="calibration_data.json"):
        """Save calibration data to file"""
        if self.is_calibrated:
            data = {
                'screen_width': self.screen_width,
                'screen_height': self.screen_height,
                'transformation_matrix': self.transformation_matrix.tolist(),
                'timestamp': datetime.now().isoformat(),
                'num_points': len(self.calibration_points)
            }
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Calibration saved to {filename}")

    def load_calibration(self, filename="calibration_data.json"):
        """Load calibration data from file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)

            self.screen_width = data['screen_width']
            self.screen_height = data['screen_height']
            self.transformation_matrix = np.array(data['transformation_matrix'])
            self.is_calibrated = True
            print(f"Calibration loaded from {filename}")
            return True
        except FileNotFoundError:
            print(f"Calibration file {filename} not found")
            return False
        except Exception as e:
            print(f"Error loading calibration: {e}")
            return False