from __future__ import division
import os
import cv2
import dlib
from .eye import Eye
from .calibration import Calibration
from .screen_calibration import ScreenCalibration
from .region_classifier import RegionClassifier
import socket
import time


class GazeTracking(object):
    """
    Enhanced gaze tracking with screen coordinates and 25-region classification
    """

    def __init__(self, screen_width=1920, screen_height=1080):
        self.frame = None
        self.eye_left = None
        self.eye_right = None
        self.calibration = Calibration()
        self.screen_calibration = ScreenCalibration(screen_width, screen_height)
        self.region_classifier = RegionClassifier()

        # Socket for sending region data to UI
        self.ui_host = '192.0.0.2'
        self.ui_port = 5051

        # _face_detector is used to detect faces
        self._face_detector = dlib.get_frontal_face_detector()

        # _predictor is used to get facial landmarks of a given face
        cwd = os.path.abspath(os.path.dirname(__file__))
        model_path = os.path.abspath(os.path.join(cwd, "trained_models/shape_predictor_68_face_landmarks.dat"))
        self._predictor = dlib.shape_predictor(model_path)

    @property
    def pupils_located(self):
        """Check that the pupils have been located"""
        try:
            int(self.eye_left.pupil.x)
            int(self.eye_left.pupil.y)
            int(self.eye_right.pupil.x)
            int(self.eye_right.pupil.y)
            return True
        except Exception:
            return False

    def _analyze(self):
        """Detects the face and initialize Eye objects"""
        frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        faces = self._face_detector(frame)

        try:
            landmarks = self._predictor(frame, faces[0])
            self.eye_left = Eye(frame, landmarks, 0, self.calibration)
            self.eye_right = Eye(frame, landmarks, 1, self.calibration)
        except IndexError:
            self.eye_left = None
            self.eye_right = None

    def refresh(self, frame):
        """Refreshes the frame and analyzes it."""
        self.frame = frame
        self._analyze()

    def pupil_left_coords(self):
        """Returns the coordinates of the left pupil"""
        if self.pupils_located:
            x = self.eye_left.origin[0] + self.eye_left.pupil.x
            y = self.eye_left.origin[1] + self.eye_left.pupil.y
            return (x, y)

    def pupil_right_coords(self):
        """Returns the coordinates of the right pupil"""
        if self.pupils_located:
            x = self.eye_right.origin[0] + self.eye_right.pupil.x
            y = self.eye_right.origin[1] + self.eye_right.pupil.y
            return (x, y)

    def horizontal_ratio(self):
        """Returns a number between 0.0 and 1.0 for horizontal gaze direction"""
        if self.pupils_located:
            pupil_left = self.eye_left.pupil.x / (self.eye_left.center[0] * 2 - 10)
            pupil_right = self.eye_right.pupil.x / (self.eye_right.center[0] * 2 - 10)
            return (pupil_left + pupil_right) / 2

    def vertical_ratio(self):
        """Returns a number between 0.0 and 1.0 for vertical gaze direction"""
        if self.pupils_located:
            pupil_left = self.eye_left.pupil.y / (self.eye_left.center[1] * 2 - 10)
            pupil_right = self.eye_right.pupil.y / (self.eye_right.center[1] * 2 - 10)
            return (pupil_left + pupil_right) / 2

    def get_normalized_coordinates(self):
        """Get normalized coordinates (0.0-1.0) for region classification"""
        h_ratio = self.horizontal_ratio()
        v_ratio = self.vertical_ratio()

        if h_ratio is None or v_ratio is None:
            return None, None

        # Clamp to 0.0-1.0 range
        norm_x = max(0.0, min(1.0, h_ratio))
        norm_y = max(0.0, min(1.0, v_ratio))

        return norm_x, norm_y

    def get_region(self):
        """Get the current 25-region classification"""
        norm_x, norm_y = self.get_normalized_coordinates()

        if norm_x is None or norm_y is None:
            return None

        return self.region_classifier.classify_point(norm_x, norm_y)

    def get_region_name(self):
        """Get human-readable region name"""
        region = self.get_region()
        if region:
            return self.region_classifier.get_region_name(region)
        return "unknown"

    def send_region_to_ui(self, region_value):
        """Send region value to UI via socket"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1.0)  # 1 second timeout
                s.connect((self.ui_host, self.ui_port))
                s.sendall(f"{region_value}\n".encode())
                print(f"[INFO] Sent region {region_value} to UI")
                return True
        except Exception as e:
            print(f"[ERROR] Failed to send region to UI: {e}")
            return False

    def get_screen_coordinates(self):
        """Get predicted screen coordinates"""
        if not self.pupils_located:
            return None

        h_ratio = self.horizontal_ratio()
        v_ratio = self.vertical_ratio()
        left_pupil = self.pupil_left_coords()
        right_pupil = self.pupil_right_coords()

        return self.screen_calibration.predict_screen_position(
            h_ratio, v_ratio, left_pupil, right_pupil
        )

    def add_calibration_point(self, screen_x, screen_y):
        """Add calibration point during calibration process"""
        if not self.pupils_located:
            return False

        self.screen_calibration.add_calibration_point(
            screen_x, screen_y,
            self.pupil_left_coords(),
            self.pupil_right_coords(),
            self.horizontal_ratio(),
            self.vertical_ratio()
        )
        return True

    def complete_calibration(self):
        """Complete the calibration process"""
        return self.screen_calibration.calculate_transformation()

    # Original methods for compatibility
    def is_right(self):
        """Returns true if the user is looking to the right"""
        if self.pupils_located:
            return self.horizontal_ratio() <= 0.35

    def is_left(self):
        """Returns true if the user is looking to the left"""
        if self.pupils_located:
            return self.horizontal_ratio() >= 0.65

    def is_center(self):
        """Returns true if the user is looking to the center"""
        if self.pupils_located:
            return self.is_right() is not True and self.is_left() is not True

    def is_blinking(self):
        """Returns true if the user closes his eyes"""
        if self.pupils_located:
            blinking_ratio = (self.eye_left.blinking + self.eye_right.blinking) / 2
            return blinking_ratio > 3.8

    def annotated_frame(self):
        """Returns the main frame with pupils highlighted"""
        frame = self.frame.copy()

        if self.pupils_located:
            color = (0, 255, 0)
            x_left, y_left = self.pupil_left_coords()
            x_right, y_right = self.pupil_right_coords()
            cv2.line(frame, (x_left - 5, y_left), (x_left + 5, y_left), color)
            cv2.line(frame, (x_left, y_left - 5), (x_left, y_left + 5), color)
            cv2.line(frame, (x_right - 5, y_right), (x_right + 5, y_right), color)
            cv2.line(frame, (x_right, y_right - 5), (x_right, y_right + 5), color)

        return frame