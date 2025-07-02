import cv2

image = cv2.imread('bot.png')

g_tint = image.copy()
g_tint[:, :, 0] = 0
g_tint[:, :, 2] = 0

cv2.imshow("Green Tint Filter", g_tint)

cv2.waitKey(0)
cv2.destroyAllWindows()
