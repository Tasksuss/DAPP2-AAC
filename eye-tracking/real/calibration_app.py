import cv2
import numpy as np
from gaze_tracking import GazeTracking


class CalibrationApp:
    def __init__(self):
        self.gaze = GazeTracking()
        self.webcam = cv2.VideoCapture(0)
        # 5-point calibration: corners + center
        self.calibration_points = [
            (960, 540),  # Center (most important)
            (300, 300),  # Top-left
            (1620, 300),  # Top-right
            (300, 780),  # Bottom-left
            (1620, 780),  # Bottom-right
        ]
        self.current_point = 0
        self.samples_collected = 0
        self.samples_needed = 20  # Reduced from 30 to 20 for faster calibration

    def run_calibration(self):
        """Run the 5-point calibration process"""
        cv2.namedWindow('Calibration', cv2.WINDOW_FULLSCREEN)

        while self.current_point < len(self.calibration_points):
            ret, frame = self.webcam.read()
            if not ret:
                continue

            self.gaze.refresh(frame)

            # Create calibration display
            display = np.zeros((1080, 1920, 3), dtype=np.uint8)

            # Draw calibration point with animation
            point = self.calibration_points[self.current_point]

            # Animated circle for better user attention
            radius = 15 + int(5 * np.sin(self.samples_collected * 0.3))
            cv2.circle(display, point, radius, (0, 255, 0), -1)
            cv2.circle(display, point, radius + 5, (255, 255, 255), 2)

            # Show which point we're on
            point_names = ["Center", "Top-Left", "Top-Right", "Bottom-Left", "Bottom-Right"]
            current_name = point_names[self.current_point]

            # Instructions
            text = f"Look at the GREEN circle - {current_name}"
            cv2.putText(display, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            progress_text = f"Point {self.current_point + 1}/5 - Samples: {self.samples_collected}/{self.samples_needed}"
            cv2.putText(display, progress_text, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            # Progress bar
            bar_width = 400
            bar_height = 20
            bar_x = 50
            bar_y = 120

            # Background bar
            cv2.rectangle(display, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (100, 100, 100), -1)

            # Progress bar
            progress_width = int((self.samples_collected / self.samples_needed) * bar_width)
            cv2.rectangle(display, (bar_x, bar_y), (bar_x + progress_width, bar_y + bar_height), (0, 255, 0), -1)

            # Collect samples
            if self.gaze.pupils_located:
                if self.gaze.add_calibration_point(point[0], point[1]):
                    self.samples_collected += 1

                if self.samples_collected >= self.samples_needed:
                    self.current_point += 1
                    self.samples_collected = 0

                    # Show completion message for current point
                    if self.current_point < len(self.calibration_points):
                        cv2.putText(display, f"{current_name} Complete! Moving to next point...",
                                    (50, 1000), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                # Show warning if eyes not detected
                cv2.putText(display, "Eyes not detected - please look at the camera",
                            (50, 950), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

            cv2.imshow('Calibration', display)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:  # Q or ESC to quit
                break
            elif key == ord('r'):  # R to restart current point
                self.samples_collected = 0

        # Show completion screen
        if self.current_point >= len(self.calibration_points):
            display = np.zeros((1080, 1920, 3), dtype=np.uint8)
            cv2.putText(display, "Calibration Complete!", (600, 400), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
            cv2.putText(display, "Processing calibration data...", (650, 500), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 255, 255), 2)
            cv2.imshow('Calibration', display)
            cv2.waitKey(2000)  # Show for 2 seconds

        # Complete calibration
        success = self.gaze.complete_calibration()

        # Show result
        display = np.zeros((1080, 1920, 3), dtype=np.uint8)
        if success:
            cv2.putText(display, "Calibration Successful!", (600, 400), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
            cv2.putText(display, "Press any key to start tracking", (650, 500), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 255, 255), 2)
            print("5-point calibration completed successfully!")
        else:
            cv2.putText(display, "Calibration Failed!", (650, 400), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
            cv2.putText(display, "Not enough data points collected", (600, 500), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 255, 255), 2)
            cv2.putText(display, "Press any key to exit", (700, 600), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            print("Calibration failed. Not enough data points.")

        cv2.imshow('Calibration', display)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return success


if __name__ == "__main__":
    app = CalibrationApp()
    app.run_calibration()