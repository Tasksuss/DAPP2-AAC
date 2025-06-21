import cv2
import time
from gaze_tracking import GazeTracking


def main():
    # Initialize enhanced gaze tracking
    gaze = GazeTracking()
    webcam = cv2.VideoCapture(0)

    print("Enhanced Eye Tracking with 25-Region Classification")
    print("Features:")
    print("- Screen coordinate mapping")
    print("- 25-region classification")
    print("- Socket communication to UI")
    print("- Original directional detection")
    print("\nPress 'c' to calibrate, 'q' to quit, 'r' to show regions")

    # Optional: Run calibration first
    calibrate = input("Run calibration first? (y/n): ").lower() == 'y'
    if calibrate:
        from calibration_app import CalibrationApp
        calibration_app = CalibrationApp()
        success = calibration_app.run_calibration()
        if not success:
            print("Calibration failed, continuing without screen mapping...")

    last_region_send = time.time()

    while True:
        ret, frame = webcam.read()
        if not ret:
            continue

        gaze.refresh(frame)
        frame = gaze.annotated_frame()

        # Get all tracking information
        region = gaze.get_region()
        region_name = gaze.get_region_name()
        screen_pos = gaze.get_screen_coordinates()
        norm_x, norm_y = gaze.get_normalized_coordinates()

        # Display gaze direction (original functionality)
        if gaze.is_blinking():
            text = "Blinking"
            color = (0, 0, 255)
        elif gaze.is_right():
            text = "Looking right"
            color = (255, 0, 0)
        elif gaze.is_left():
            text = "Looking left"
            color = (0, 255, 255)
        elif gaze.is_center():
            text = "Looking center"
            color = (0, 255, 0)
        else:
            text = "Eyes not detected"
            color = (128, 128, 128)

        cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.2, color, 2)

        # Display region information
        if region:
            region_text = f"Region: {region} ({region_name})"
            cv2.putText(frame, region_text, (90, 100), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 0), 2)

            # Send region to UI every 0.5 seconds
            current_time = time.time()
            if current_time - last_region_send > 0.5:
                gaze.send_region_to_ui(region)
                last_region_send = current_time

        # Display normalized coordinates
        if norm_x is not None and norm_y is not None:
            norm_text = f"Normalized: ({norm_x:.3f}, {norm_y:.3f})"
            cv2.putText(frame, norm_text, (90, 140), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 0), 1)

        # Display screen coordinates (if calibrated)
        if screen_pos:
            screen_text = f"Screen: ({screen_pos[0]}, {screen_pos[1]})"
            cv2.putText(frame, screen_text, (90, 180), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 0, 255), 2)

        # Display pupil coordinates
        left_pupil = gaze.pupil_left_coords()
        right_pupil = gaze.pupil_right_coords()
        if left_pupil and right_pupil:
            cv2.putText(frame, f"Left pupil: {left_pupil}", (90, 220), cv2.FONT_HERSHEY_DUPLEX, 0.6, (147, 58, 31), 1)
            cv2.putText(frame, f"Right pupil: {right_pupil}", (90, 250), cv2.FONT_HERSHEY_DUPLEX, 0.6, (147, 58, 31), 1)

        cv2.imshow("Enhanced Eye Tracking", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:  # Q or ESC
            break
        elif key == ord('c'):  # Calibrate
            print("Starting calibration...")
            from calibration_app import CalibrationApp
            calibration_app = CalibrationApp()
            calibration_app.run_calibration()
        elif key == ord('r'):  # Show regions
            print(gaze.region_classifier.visualize_regions())

    webcam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()