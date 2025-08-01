import cv2
import numpy as np

image1 = cv2.imread('/Users/abedard/Desktop/MATT technique/Test13juin/Frames/Zero degrée/P4_JD_5N.jpg', cv2.IMREAD_GRAYSCALE)
image2 = cv2.imread('/Users/abedard/Desktop/MATT technique/Test13juin/Frames/Zero degrée/P4_JD_5.jpg', cv2.IMREAD_GRAYSCALE)

def select_roi(image, window_name):
    roi = cv2.selectROI(window_name, image)
    cv2.destroyWindow(window_name)
    return roi

roi1 = select_roi(image1, "Select ROI for Image 1")
roi2 = select_roi(image2, "Select ROI for Image 2")

x1, y1, w1, h1 = roi1
cropped_image1 = image1[y1:y1+h1, x1:x1+w1]

x2, y2, w2, h2 = roi2
cropped_image2 = image2[y2:y2+h2, x2:x2+w2]

# Detect ORB keypoints and descriptors
orb = cv2.ORB_create()
keypoints1, descriptors1 = orb.detectAndCompute(cropped_image1, None)
keypoints2, descriptors2 = orb.detectAndCompute(cropped_image2, None)

if descriptors1 is None or descriptors2 is None:
    print("Not enough keypoints detected.")
    exit(1)

bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.match(descriptors1, descriptors2)

# Check if enough matches are found
if len(matches) < 4:
    print("Not enough matches found.")
    exit(1)

# Sort matches by distance
matches = sorted(matches, key=lambda x: x.distance)

# Extract location of good matches
points1 = np.zeros((len(matches), 2), dtype=np.float32)
points2 = np.zeros((len(matches), 2), dtype=np.float32)

for i, match in enumerate(matches):
    points1[i, :] = keypoints1[match.queryIdx].pt
    points2[i, :] = keypoints2[match.trainIdx].pt

# Find homography
h, mask = cv2.findHomography(points2, points1, cv2.RANSAC)

# Use homography to warp the second image
height, width = cropped_image1.shape
aligned_image2 = cv2.warpPerspective(cropped_image2, h, (width, height))

# Create a window to display the overlay
cv2.namedWindow('Overlay')

# Callback function for the trackbar
def update_overlay(alpha_slider):
    alpha = alpha_slider / 100.0
    overlay = cv2.addWeighted(cropped_image1, 1 - alpha, aligned_image2, alpha, 0)
    cv2.imshow('Overlay', overlay)

# Create a trackbar to adjust the transparency
cv2.createTrackbar('Transparency', 'Overlay', 50, 100, update_overlay)

# Initial call to display the image
update_overlay(50)

print(f'X translation: {h[0, 2]} pixels')
print(f'Y translation: {h[1, 2]} pixels')

# Wait for the user to close the window
cv2.waitKey(0)
cv2.destroyAllWindows()