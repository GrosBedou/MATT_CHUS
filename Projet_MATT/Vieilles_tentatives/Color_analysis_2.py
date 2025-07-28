import cv2
import numpy as np

def is_circular(contour, circularity_threshold=0.75):
    perimeter = cv2.arcLength(contour, True)
    area = cv2.contourArea(contour)
    if perimeter == 0:
        return False
    circularity = 4 * np.pi * (area / (perimeter ** 2))
    return circularity > circularity_threshold

def contour_brightness(contour: np.ndarray, hsv_image: np.ndarray) -> float:
    mask = np.zeros(hsv_image.shape[:2], dtype=np.uint8)
    cv2.drawContours(mask, [contour], -1, 255, -1)
    return cv2.mean(hsv_image, mask=mask)[2]  # Return the V channel mean

cap = cv2.VideoCapture('/Users/abedard/Desktop/MATT technique/MATT 30-0.mp4')

if not cap.isOpened():
    print("Error: Failed to open video")
    cap.release()
    cv2.destroyAllWindows()
    exit()

ret, frame = cap.read()

if not ret:
    print("Error: Failed to read video frame")
    cap.release()
    cv2.destroyAllWindows()
    exit()

# Convert frame for consistent processing
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# Let user select ROI
roi = cv2.selectROI("Select Initial ROI", frame, showCrosshair=True, fromCenter=False)
cv2.destroyWindow("Select Initial ROI")

# Initialize the tracker with user-defined ROI
tracker = cv2.TrackerCSRT.create()
tracking = tracker.init(frame, roi)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Initialize mask
    mask = np.zeros(hsv.shape[:2], dtype=np.uint8)

    if tracking:
        success, bbox = tracker.update(frame)
        if success:
            x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        else:
            tracking = False
    else:
        lower_yellow = np.array([15, 100, 100])
        upper_yellow = np.array([28, 255, 255])
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = [cnt for cnt in contours if is_circular(cnt, 0.75) and cv2.contourArea(cnt) > 50]

        if contours:
            # Select contour with the highest brightness
            brightest_contour = max(contours, key=lambda cnt: contour_brightness(cnt, hsv))
            x, y, w, h = cv2.boundingRect(brightest_contour)
            tracker = cv2.TrackerCSRT.create()  # Recreate the tracker
            tracker.init(frame, (x, y, w, h))
            tracking = True

    # Visual debugging: Display the frame and mask side-by-side
    combined_display = np.hstack((frame, cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)))
    cv2.imshow('Tracking and Mask', combined_display)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()