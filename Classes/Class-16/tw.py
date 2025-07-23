import cv2
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        print("Webcam not working")
        break
    cv2.imshow("Test", frame)
    print("Reading frame")
    ret, frame = cap.read()
    if not ret:
        print("No frame received")
        break
    print("Frame received")
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()
