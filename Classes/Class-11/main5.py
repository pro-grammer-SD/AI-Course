import cv2
import numpy as np

# Load the image
image_path = 'bot.png'
image = cv2.imread(image_path)

if image is None:
    print(f"Error: Could not load image from {image_path}")
    exit()

# Convert image to float32 to allow for calculations involving negative values
# This is crucial because uint8 (0-255) would wrap around or clip immediately
# if we tried to subtract (or add negative numbers) directly.
image_float = image.astype(np.float32)

# Define the BGR color adjustment values.
# OpenCV uses BGR order, so:
# - Blue channel: Decrease by 50 (represented as -50)
# - Green channel: No change (represented as 0)
# - Red channel: Increase by 50 (represented as +50)
adjustment_bgr = np.array([-50, 0, 50], dtype=np.float32)

# Apply the adjustment using cv2.add().
# cv2.add performs element-wise addition. Since image_float is float32,
# this operation will correctly handle negative values for the blue channel.
adjusted_image_float = cv2.add(image_float, adjustment_bgr)

# Clip the values to be within the valid range [0, 255]
# This handles saturation: any value < 0 becomes 0, any value > 255 becomes 255.
# Finally, convert the image back to uint8 for display.
adjusted_image = np.clip(adjusted_image_float, 0, 255).astype(np.uint8)

# Display the original and adjusted images
cv2.imshow("Original Image", image)
cv2.imshow("Adjusted Image (Red Increased, Blue Decreased)", adjusted_image)

cv2.waitKey(0)
cv2.destroyAllWindows()
