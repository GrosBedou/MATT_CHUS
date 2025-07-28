import cv2
import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, FloatSlider

# Load the two images
# image1 = cv2.imread('/Users/abedard/Desktop/MATT technique/Test28mai/Frames/Zéro degrée/P2_JD_5.jpg', cv2.IMREAD_GRAYSCALE)
# image2 = cv2.imread('/Users/abedard/Desktop/MATT technique/Test28mai/Frames/Zéro degqrée/P2_JD_5N.jpg', cv2.IMREAD_GRAYSCALE)

image1 = cv2.imread('/Users/abedard/Desktop/MATT technique/Test28mai/Frames/30 degrée/P2_JD_5_30deg.jpg', cv2.IMREAD_GRAYSCALE)
image2 = cv2.imread('/Users/abedard/Desktop/MATT technique/Test28mai/Frames/30 degrée/P2_JD_5N_30deg.jpg', cv2.IMREAD_GRAYSCALE)

# image1 = cv2.imread('/Users/abedard/Desktop/MATT technique/Test13juin/Frames/Zero degrée/P4_JD_5N.jpg', cv2.IMREAD_GRAYSCALE)
# image2 = cv2.imread('/Users/abedard/Desktop/MATT technique/Test13juin/Frames/Zero degrée/P4_JD_5.jpg', cv2.IMREAD_GRAYSCALE)

# Detect ORB keypoints and descriptors
orb = cv2.ORB_create()
keypoints1, descriptors1 = orb.detectAndCompute(image1, None)
keypoints2, descriptors2 = orb.detectAndCompute(image2, None)

# Check if keypoints are detected
if descriptors1 is None or descriptors2 is None:
    print("Not enough keypoints detected.")
    exit(1)

# Match descriptors using BFMatcher
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
height, width = image1.shape
aligned_image2 = cv2.warpPerspective(image2, h, (width, height))

# Create a window to display the overlay
cv2.namedWindow('Overlay')

# Callback function for the trackbar
def update_overlay(alpha_slider):
    alpha = alpha_slider / 100.0
    overlay = cv2.addWeighted(image1, 1 - alpha, aligned_image2, alpha, 0)
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