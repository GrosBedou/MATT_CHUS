import cv2
import numpy as np

def is_circular(contour, circularity_threshold=0.5):  # Increase circularity threshold
    perimeter = cv2.arcLength(contour, True)
    area = cv2.contourArea(contour)
    if perimeter == 0:
        return False
    circularity = 4 * np.pi * (area / (perimeter ** 2))
    return circularity > circularity_threshold

# Update the path to your video file
video_path = '/Users/abedard/Desktop/MATT technique/MATT 30-0.mp4'
cap = cv2.VideoCapture(video_path)

# Check if video opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Read the first frame
ret, frame = cap.read()
if not ret:
    print("Error: Failed to read video")
    cap.release()
    cv2.destroyAllWindows()
    exit()

# Initialize the tracker
tracker = cv2.TrackerCSRT_create()
tracking = False  # Initially set tracking to False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    if tracking:
        # Update the tracker and draw the bounding box
        success, bbox = tracker.update(frame)
        if success:
            x, y, w, h = map(int, bbox)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        else:
            tracking = False
    else:
        # Convert to HSV and threshold for bright yellow
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_yellow = np.array([22, 100, 100])  # Adjusted lower bound
        upper_yellow = np.array([50, 255, 255])  # Adjusted upper bound
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # Morphological operations to clean up the mask
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # Added closing operation

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = [cnt for cnt in contours if 50 < cv2.contourArea(cnt) < 500 and is_circular(cnt)]

        if contours:
            # Initialize the tracker with the largest contour
            light_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(light_contour)
            tracker.init(frame, (x, y, w, h))
            tracking = True

    # Visual debugging: Display the frame and mask side-by-side
    combined_display = np.hstack((frame, cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)))
    cv2.imshow('Tracking and Mask', combined_display)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()