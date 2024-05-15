import cv2
import numpy as np

print(cv2.__version__)

# Open the video file
#cap = cv2.VideoCapture('/Users/abedard/Desktop/MATT technique/MATT 0-30°b.mp4')
cap = cv2.VideoCapture('/Users/abedard/Desktop/MATT technique/MATT 30-0.mp4')


# Initialize tracker and tracking flag
tracker = cv2.legacy.TrackerCSRT_create()
tracking = False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    if tracking:
        # Update the tracker
        success, bbox = tracker.update(frame)
        if success:
            x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        else:
            tracking = False
    else:
        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (9, 9), 0)

        # Threshold the image
        _, thresholded = cv2.threshold(blurred, 230, 255, cv2.THRESH_BINARY)

        # Find contours
        contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            # Assuming the largest contour is the circle
            circle_contour = max(contours, key=cv2.contourArea)

            # Calculate the bounding box of the circle
            x, y, w, h = cv2.boundingRect(circle_contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Initialize the tracker with the first frame and bounding box
            tracker.init(frame, (x, y, w, h))
            tracking = True

    # Display the frame
    cv2.imshow('Frame with Detected Circle', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
        break

cap.release()
cv2.destroyAllWindows()