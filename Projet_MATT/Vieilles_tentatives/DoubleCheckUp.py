import cv2
import numpy as np

def is_circular(contour, circularity_threshold=0.75):
    perimeter = cv2.arcLength(contour, True)
    area = cv2.contourArea(contour)
    if perimeter == 0:
        return False
    circularity = 4 * np.pi * (area / (perimeter ** 2))
    return circularity > circularity_threshold

def filter_by_brightness_and_color(contours, hsv_image, saturation_threshold=100, value_threshold=150):
    valid_contours = []
    for cnt in contours:
        mask = np.zeros(hsv_image.shape[:2], dtype=np.uint8)
        cv2.drawContours(mask, [cnt], -1, 255, -1)
        mean_val = cv2.mean(hsv_image, mask=mask)
        if mean_val[1] >= saturation_threshold and mean_val[2] >= value_threshold:
            valid_contours.append(cnt)
    return valid_contours

cap = cv2.VideoCapture('/Users/abedard/Desktop/MATT technique/MATT 30-0.mp4')
ret, frame = cap.read()

if not ret:
    print("Error: Failed to read video")
    cap.release()
    cv2.destroyAllWindows()
    exit()

# Let user select ROI
roi = cv2.selectROI("Select Initial ROI", frame, showCrosshair=True, fromCenter=False)
cv2.destroyWindow("Select Initial ROI")
tracker = cv2.TrackerCSRT_create()
x, y, w, h = roi
if w > 0 and h > 0:
    tracking = tracker.init(frame, roi)
    if not tracking:
        print("Tracker initialization failed.")
else:
    print("Invalid ROI selected.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    if tracking:
        success, bbox = tracker.update(frame)
        if success:
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (0, 255, 0), 2)  # Green rectangle to show tracking
        else:
            print("Tracking failed on this frame.")
            tracking = False
    else:
        print("Tracking not initialized or stopped.")

    cv2.imshow('Tracking', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()