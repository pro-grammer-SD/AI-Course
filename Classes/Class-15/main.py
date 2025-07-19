import cv2
import mediapipe as mp
import time
import screen_brightness_control as sbc
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

base_options = python.BaseOptions(model_asset_path='gesture_recognizer.task')
options = vision.GestureRecognizerOptions(base_options=base_options)
recognizer = vision.GestureRecognizer.create_from_options(options)

cap = cv2.VideoCapture(0)

last_gesture = None
last_time = 0
cooldown = 0.2  

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    result = recognizer.recognize(mp_image)

    if result.gestures:
        gesture = result.gestures[0][0].category_name
        current_time = time.time()

        if gesture != last_gesture or (current_time - last_time) > cooldown:
            if gesture == "Thumb_Up":
                sbc.set_brightness(min(sbc.get_brightness()[0] + 10, 100))
                last_time = current_time

            elif gesture == "Thumb_Down":
                sbc.set_brightness(max(sbc.get_brightness()[0] - 10, 0))
                last_time = current_time

            elif gesture == "Open_Palm":
                vol = volume.GetMasterVolumeLevelScalar()
                volume.SetMasterVolumeLevelScalar(max(vol + 0.05, 0.0), None)
                last_time = current_time

            elif gesture == "Closed_Fist":
                vol = volume.GetMasterVolumeLevelScalar()
                volume.SetMasterVolumeLevelScalar(max(vol - 0.05, 0.0), None)
                last_time = current_time
            
            last_gesture = gesture

        cv2.putText(frame, f'Gesture: {gesture}', (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Gesture Recognition", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
