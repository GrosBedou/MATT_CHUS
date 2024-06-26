import cv2
import numpy as np
from matplotlib import pyplot as plt

# Load the image
image_path = '/Users/abedard/Desktop/peepoopoo.jpg'
image = cv2.imread(image_path)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Define ROI (you may need to adjust the coordinates based on your image)
roi = gray[200:600, 490:900]

# Apply Bilateral Filter to reduce noise while keeping edges sharp
bilateral_filtered = cv2.bilateralFilter(roi, 9, 75, 75)

# Apply adaptive thresholding
thresh = cv2.adaptiveThreshold(bilateral_filtered, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY_INV, 11, 2)

# Apply more aggressive morphological operations to remove noise
kernel = np.ones((7, 7), np.uint8)
morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

# Use Canny edge detection
edges = cv2.Canny(morph, 50, 150)

# Find contours
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Draw contours on the original image
contour_image = image.copy()
roi_color = contour_image[200:600, 490:900]

# Define parameters for the large ellipse
center_coordinates = (roi_color.shape[1]//2, roi_color.shape[0]//2)
axes_lengths = (roi_color.shape[1]//2 - 10, roi_color.shape[0]//2 - 10)  # Adjust as necessary
angle = 0
startAngle = 0
endAngle = 360

# Draw the large ellipse
cv2.ellipse(roi_color, center_coordinates, axes_lengths, angle, startAngle, endAngle, (0, 0, 255), 2)

# Display the results
plt.figure(figsize=(12, 6))
plt.subplot(1, 3, 1)
plt.title("Original Image")
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')

plt.subplot(1, 3, 2)
plt.title("Adaptive Thresholding")
plt.imshow(thresh, cmap='gray')
plt.axis('off')

plt.subplot(1, 3, 3)
plt.title("Contours with Large Ellipse")
plt.imshow(cv2.cvtColor(contour_image, cv2.COLOR_BGR2RGB))
plt.axis('off')

plt.show()