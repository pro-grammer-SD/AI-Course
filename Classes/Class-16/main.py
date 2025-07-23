import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import pyautogui

model_path = 'gr.task' 

base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.GestureRecognizerOptions(base_options=base_options)

recognizer = vision.GestureRecognizer.create_from_options(options)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    recognition_result = recognizer.recognize(mp_image)

    if recognition_result.gestures:
        for gesture in recognition_result.gestures:
            category_name = gesture[0].category_name
            score = gesture[0].score
            cv2.putText(frame, f'Gesture: {category_name} ({score:.2f})', (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            if category_name == "Open_Palm":
                pyautogui.scroll(100)
            elif category_name == "Closed_Fist":
                pyautogui.scroll(-100)
            
    cv2.imshow('Gesture Recognition', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
