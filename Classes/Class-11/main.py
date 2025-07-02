import cv2
import numpy as np

# Load the image
image = cv2.imread('bot.png')

if image is None:
    print("Error: Could not load image. Make sure 'bot.png' is in the same directory.")
else:
    # Split the image into its B, G, R channels
    b, g, r = cv2.split(image)

    # Define the intensity changes
    red_increase_value = 50  # Value to add to the red channel
    blue_decrease_value = 50 # Value to subtract from the blue channel

    # Create matrices for addition and subtraction
    # Ensure they are of the same data type as the image channels (e.g., np.uint8)
    red_add_matrix = np.full(r.shape, red_increase_value, dtype=np.uint8)
    blue_subtract_matrix = np.full(b.shape, blue_decrease_value, dtype=np.uint8)

    # Increase red channel using cv2.add()
    # cv2.add handles saturation (caps at 255)
    r_increased = cv2.add(r, red_add_matrix)

    # Decrease blue channel using cv2.subtract()
    # cv2.subtract handles underflow (caps at 0)
    b_decreased = cv2.subtract(b, blue_subtract_matrix)

    # Merge the modified channels back
    modified_image = cv2.merge([b_decreased, g, r_increased])

    # Display the original and modified images
    cv2.imshow("Original Image", image)
    cv2.imshow("Red Increased, Blue Decreased", modified_image)

    # Wait for a key press and then close all windows
    cv2.waitKey(0)
    cv2.destroyAllWindows()
