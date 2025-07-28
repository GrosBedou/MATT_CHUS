import cv2
import numpy as np

# Open the video file
cap = cv2.VideoCapture('/Users/abedard/Desktop/MATT technique/MATT 0-30°b.mp4')

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray, (9, 9), 0)

    # Threshold the image
    _, thresholded = cv2.threshold(blurred, 245, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Assuming the largest contour is the circle
        circle_contour = max(contours, key=cv2.contourArea)

        # Calculate the centroid and bounding box of the circle
        M = cv2.moments(circle_contour)
        if M["m00"] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            # Draw the centroid
            cv2.circle(frame, (cx, cy), 7, (255, 0, 0), -1)
            import cv2
            import numpy as np

            # Open the video file
            cap = cv2.VideoCapture('/Users/abedard/Desktop/MATT technique/MATT 0-30°b.mp4')

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                # Convert frame to grayscale
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Apply Gaussian blur
                blurred = cv2.GaussianBlur(gray, (9, 9), 0)

                # Threshold the image
                _, thresholded = cv2.threshold(blurred, 245, 255, cv2.THRESH_BINARY)

                # Find contours
                contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                if contours:
                    # Assuming the largest contour is the circle
                    circle_contour = max(contours, key=cv2.contourArea)

                    # Calculate the centroid and bounding box of the circle
                    M = cv2.moments(circle_contour)
                    if M["m00"] != 0:
                        cx = int(M['m10'] / M['m00'])
                        cy = int(M['m01'] / M['m00'])
                        # Draw the centroid
                        cv2.circle(frame, (cx, cy), 7, (255, 0, 0), -1)

                        # Draw the contour
                        cv2.drawContours(frame, [circle_contour], -1, (0, 255, 0), 2)

                        x, y, w, h = cv2.boundingRect(circle_contour)
                        # Draw the bounding box
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

                # Display the frame
                cv2.imshow('Frame with Detected Circle', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
                    break

            cap.release()
            cv2.destroyAllWindows()
            # Draw the contour
            cv2.drawContours(frame, [circle_contour], -1, (0, 255, 0), 2)

            x, y, w, h = cv2.boundingRect(circle_contour)
            # Draw the bounding box
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

    # Display the frame
    cv2.imshow('Frame with Detected Circle', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
        break

cap.release()
cv2.destroyAllWindows()