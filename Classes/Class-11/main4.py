import cv2

image = cv2.imread('bot.png')

r_tint = image.copy()
r_tint[:, :, 0] = 0
r_tint[:, :, 1] = 0

cv2.imshow("Red Tint Filter", r_tint)

cv2.waitKey(0)
cv2.destroyAllWindows()
