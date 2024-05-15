import cv2

cap = cv2.VideoCapture('/Users/abedard/Desktop/MATT technique/MATT 0-30°b.mp4')
#cap = cv2.VideoCapture('/Users/abedard/Desktop/MATT technique/MATT 30-0.mp4')
# Initialisation du tracker
tracker = cv2.TrackerCSRT_create()
tracking = False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    if tracking:
        # Update tracker avec l'image d'avant
        success, bbox = tracker.update(frame)
        if success:
            x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            # Centroid de la lumière
            cx, cy = x + w // 2, y + h // 2
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
        else:
            tracking = False
    else:
        # Toute gris
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Gaussian blur, permet de mieux voir les formes et définir le cercle lumineux
        blurred = cv2.GaussianBlur(gray, (9, 9), 0)

        # Threshold the image
        _, thresholded = cv2.threshold(blurred, 230, 255, cv2.THRESH_BINARY)

        # Contours
        contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            # Assuming the largest contour is the circle
            circle_contour = max(contours, key=cv2.contourArea)

            # Calculate the bounding box of the circle
            x, y, w, h = cv2.boundingRect(circle_contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Calculate and draw the centroid
            M = cv2.moments(circle_contour)
            if M["m00"] != 0:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

            # Initialize the tracker with the first frame and bounding box
            tracker.init(frame, (x, y, w, h))
            tracking = True

    # Display the frame
    cv2.imshow('Frame with Detected Circle', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
        break

cap.release()
cv2.destroyAllWindows()