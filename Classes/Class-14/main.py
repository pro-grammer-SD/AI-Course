import cv2
import numpy as np
import collections

cap = cv2.VideoCapture(0)
gesture_history = collections.deque(maxlen=7)

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    roi = frame[100:400, 100:400]
    cv2.rectangle(frame, (100, 100), (400, 400), (0, 255, 0), 2)

    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    lower_skin = np.array([0, 30, 60], dtype=np.uint8)
    upper_skin = np.array([20, 150, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower_skin, upper_skin)

    mask = cv2.GaussianBlur(mask, (11, 11), 0)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    gesture = ""
    if contours:
        cnt = max(contours, key=cv2.contourArea)
        if cv2.contourArea(cnt) > 5000:
            hull = cv2.convexHull(cnt)
            hull_indices = cv2.convexHull(cnt, returnPoints=False)
            defects = cv2.convexityDefects(cnt, hull_indices)

            count_defects = 0
            if defects is not None:
                for i in range(defects.shape[0]):
                    s, e, f, d = defects[i, 0]
                    start = tuple(cnt[s][0])
                    end = tuple(cnt[e][0])
                    far = tuple(cnt[f][0])

                    a = np.linalg.norm(np.array(start) - np.array(end))
                    b = np.linalg.norm(np.array(start) - np.array(far))
                    c = np.linalg.norm(np.array(end) - np.array(far))
                    angle = np.arccos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c + 1e-5)) * 57

                    if angle <= 90:
                        count_defects += 1
                        cv2.circle(roi, far, 5, [255, 0, 0], -1)

            if count_defects == 0:
                gesture = "1 Finger"
            elif count_defects == 1:
                gesture = "2 Fingers"
            elif count_defects == 2:
                gesture = "3 Fingers"
            elif count_defects == 3:
                gesture = "4 Fingers"
            elif count_defects >= 4:
                gesture = "5 Fingers"

            gesture_history.append(gesture)
            stable_gesture = max(set(gesture_history), key=gesture_history.count)

            cv2.putText(frame, stable_gesture, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

    cv2.imshow("Hand", frame)
    cv2.imshow("Mask", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
