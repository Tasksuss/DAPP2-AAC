import cv2
from scipy.spatial import distance as dist

# Load the eye classifiers from OpenCV
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Open video capture
cap = cv2.VideoCapture("example 2.mov")  # Change to video file path if needed

def calculate_ear(eye):
    # Compute the euclidean distances between the vertical eye landmarks
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    # Compute the euclidean distance between the horizontal eye landmarks
    C = dist.euclidean(eye[0], eye[3])
    # Compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)
    return ear


while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect eyes in the face region
    eyes = eye_cascade.detectMultiScale(gray,1.3,5)
    for (ex, ey, ew, eh) in eyes:
        eye = frame[ey:ey + eh, ex:ex + ew + 200]  # Extract eye region
        # cv2.rectangle(frame, (ex, ey+50),  (ex + ew+200, ey + eh-50), (0, 255, 0), 2)
        cv2.imshow("Eye", eye)
        break  # Show only one eye (remove if both needed)
        eye_landmarks = [
            (ex, ey + eh // 2),  # p1
            (ex + ew // 3, ey),  # p2
            (ex + 2 * ew // 3, ey),  # p3
            (ex + ew, ey + eh // 2),  # p4
            (ex + 2 * ew // 3, ey + eh),  # p5
            (ex + ew // 3, ey + eh)  # p6
        ]

        # Calculate EAR
        ear = calculate_ear(eye_landmarks)
        text = ear
        cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Press ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
