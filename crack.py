import cv2
import numpy as np

# Load the image
image_path = "concrete-crack.jpg"  # Replace with your image path
image = cv2.imread(image_path, cv2.IMREAD_COLOR)

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian Blur to reduce noise and improve edge detection
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Apply Canny Edge Detection
edges = cv2.Canny(blurred, threshold1=50, threshold2=150)

# Create a mask from the edges detected
mask = np.zeros_like(image)
mask[edges != 0] = [0, 0, 255]  # Red color for highlighting

# Overlay the mask on the original image
highlighted_image = cv2.addWeighted(image, 0.65, mask, 0.35, 0)

# Display the images
cv2.imshow("Original Image", image)
cv2.imshow("Edges Detected", edges)
cv2.imshow("Crack Highlighted", highlighted_image)

# Wait for a key press and close the windows
cv2.waitKey(0)
cv2.destroyAllWindows()

# Save the highlighted image
cv2.imwrite("highlighted_crack.jpg", highlighted_image)
