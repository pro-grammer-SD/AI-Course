import time
import threading
import os
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import pyautogui
from PIL import Image

model_path = 'gr.task'

base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.GestureRecognizerOptions(base_options=base_options)
recognizer = vision.GestureRecognizer.create_from_options(options)

cap = cv2.VideoCapture(0)

def apply_filter(frame, filter_type):
    if filter_type == 'GRAYSCALE':
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    elif filter_type == 'SEPIA':
        sepia_filter = np.array([[0.272, 0.534, 0.131],
                                 [0.349, 0.686, 0.168],
                                 [0.393, 0.769, 0.189]])
        sepia_frame = cv2.transform(frame, sepia_filter)
        return np.clip(sepia_frame, 0, 255).astype(np.uint8)
    elif filter_type == 'NEGATIVE':
        return cv2.bitwise_not(frame)
    elif filter_type == 'BLUR':
        return cv2.GaussianBlur(frame, (15, 15), 0)
    return frame

def snap_window(window_name, current_filter):
    time.sleep(2)
    window = pyautogui.getWindowsWithTitle(window_name)
    if window:
        bbox = window[0].box
        snap = pyautogui.screenshot(region=bbox)

        os.makedirs('screenshots', exist_ok=True)
        path = f"screenshots/snap_{current_filter}.png"
        snap.save(path)
        img = Image.open(path)
        img.show()

current_filter = None
screenshot_flags = {
    'GRAYSCALE': False,
    'SEPIA': False,
    'NEGATIVE': False,
    'BLUR': False
}

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
                current_filter = 'GRAYSCALE'
            elif category_name == "Closed_Fist":
                current_filter = 'SEPIA'
            elif category_name == "Thumb_Up":
                current_filter = 'NEGATIVE'
            elif category_name == 'Thumb_Down':
                current_filter = 'BLUR'
            else:
                current_filter = None

            if current_filter:
                frame = apply_filter(frame, current_filter)

                if not screenshot_flags[current_filter]:
                    screenshot_flags[current_filter] = True
                    threading.Thread(target=snap_window, args=('Gesture Recognition', current_filter)).start()

    cv2.imshow('Gesture Recognition', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
