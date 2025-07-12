import cv2
import numpy as np

img = cv2.imread("bot.png")
mode = 'o'

print("Press the following keys to apply filters:")
print("r - Red Tint")
print("g - Green Tint")
print("b - Blue Tint")
print("s - Sobel Edge Detection")
print("c - Canny Edge Detection")
print("o - Original")
print("q - Quit")

while True:
    frame = img.copy()

    if mode == 'r':
        frame = cv2.merge([np.zeros_like(frame[:, :, 0]), np.zeros_like(frame[:, :, 1]), frame[:, :, 2]])
    elif mode == 'g':
        frame = cv2.merge([np.zeros_like(frame[:, :, 0]), frame[:, :, 1], np.zeros_like(frame[:, :, 2])])
    elif mode == 'b':
        frame = cv2.merge([frame[:, :, 0], np.zeros_like(frame[:, :, 1]), np.zeros_like(frame[:, :, 2])])
    elif mode == 's':
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1)
        frame = cv2.convertScaleAbs(np.sqrt(sobelx**2 + sobely**2))
    elif mode == 'c':
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.Canny(gray, 100, 200)

    cv2.imshow("Bot Image", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    elif key in [ord('r'), ord('g'), ord('b'), ord('s'), ord('c'), ord('o')]:
        mode = chr(key)

cv2.destroyAllWindows()
