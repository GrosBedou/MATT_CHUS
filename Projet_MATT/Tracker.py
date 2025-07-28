import cv2
import numpy as np
import pandas as pd

def is_circular(contour, circularity_threshold=0.4):
    perimeter = cv2.arcLength(contour, True)
    area = cv2.contourArea(contour)
    if perimeter == 0:
        return False
    circularity = 4 * np.pi * (area / (perimeter ** 2))
    return circularity > circularity_threshold

def video_analyser(video_path, pixels_per_cm, yellowUp, yellowLower, ref_x, ref_y):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return pd.DataFrame()

    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to read video")
        cap.release()
        return pd.DataFrame()

    tracker = cv2.TrackerCSRT_create()
    tracking = False

    positions_df = pd.DataFrame(columns=['x_cm', 'y_cm', 'time'])

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_index = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        current_time = frame_index / fps

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_yellow = np.array(yellowLower)
        upper_yellow = np.array(yellowUp)
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = [cnt for cnt in contours if 50 < cv2.contourArea(cnt) < 2000 and is_circular(cnt, 0.5)]

        if contours:
            light_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(light_contour)

            if tracking:
                success, bbox = tracker.update(frame)
                if success:
                    x, y, w, h = map(int, bbox)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    x_cm = (x + w / 2 - ref_x) / pixels_per_cm
                    y_cm = (y + h / 2 - ref_y) / pixels_per_cm
                    new_row = pd.DataFrame({'x_cm': [x_cm], 'y_cm': [y_cm], 'time': [current_time]})
                    positions_df = pd.concat([positions_df, new_row], ignore_index=True)
                else:
                    tracking = False
            else:
                tracker.init(frame, (x, y, w, h))
                tracking = True
        else:
            tracking = False

        for pos in positions_df.itertuples():
            cv2.circle(frame, (int((pos.x_cm * pixels_per_cm) + ref_x), int((pos.y_cm * pixels_per_cm) + ref_y)), 2, (0, 0, 255), -1)

        combined_display = np.hstack((frame, cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)))
        cv2.imshow('Tracking and Mask', combined_display)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_index += 1

    cap.release()
    cv2.destroyAllWindows()
    print(positions_df)
    return positions_df

# Print the DataFrame
# print(positions_df)