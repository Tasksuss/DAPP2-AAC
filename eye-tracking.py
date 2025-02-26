import cv2
import pyautogui
from gaze_tracking import GazeTracking

# Initialize gaze tracking and webcam
gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

# Configuration parameters
SMOOTHING_FACTOR = 0.8  # Between 0 and 1 (higher = smoother)
MOVEMENT_SCALE = 30     # Adjust sensitivity of eye movement to mouse movement

# Get screen dimensions
screen_width, screen_height = pyautogui.size()

# Calculate screen center
center_x, center_y = screen_width // 2, screen_height // 2

# Initialize variables for smoothing
prev_x, prev_y = 0, 0  # Start at the center (0,0) in the new coordinate system

while True:
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""

    if gaze.is_blinking():
        text = "Blinking"
    elif gaze.is_right():
        text = "Looking right"
    elif gaze.is_left():
        text = "Looking left"
    elif gaze.is_center():
        text = "Looking center"

    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    # Analyze the frame using GazeTracking
    gaze.refresh(frame)
    frame = gaze.annotated_frame()

    # Get the pupil coordinates
    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()

    # Use left pupil coordinates if available
    if left_pupil is not None:
        # Map pupil coordinates to screen coordinates
        screen_x = int((left_pupil[0] / frame.shape[1]) * screen_width)
        screen_y = int((left_pupil[1] / frame.shape[0]) * screen_height)

        # Invert the x-axis movement
        inverted_x = screen_width - screen_x

        # Adjust coordinates so that center of the screen is (0,0)
        adjusted_x = inverted_x - center_x
        adjusted_y = screen_y - center_y

        # Apply movement scaling
        adjusted_x = int(adjusted_x * MOVEMENT_SCALE)
        adjusted_y = int(adjusted_y * MOVEMENT_SCALE)

        # Apply smoothing to the mouse movement
        smoothed_x = int(prev_x * SMOOTHING_FACTOR + adjusted_x * (1 - SMOOTHING_FACTOR))
        smoothed_y = int(prev_y * SMOOTHING_FACTOR + adjusted_y * (1 - SMOOTHING_FACTOR))

        # Move the mouse cursor
        pyautogui.moveTo(center_x + smoothed_x, center_y + smoothed_y)

        # Update previous position for smoothing
        prev_x, prev_y = smoothed_x, smoothed_y

    # Display the annotated frame
    cv2.imshow("Demo", frame)

    # Exit on pressing the 'Esc' key
    if cv2.waitKey(1) == 27:
        break

# Release the webcam and close the window
webcam.release()
cv2.destroyAllWindows()
