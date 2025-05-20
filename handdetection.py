
from picamera2 import Picamera2
import time
import cv2
import mediapipe as mp

# settings mediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# settings Picamera2
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()
time.sleep(2) # wait camera safe

# MediaPipe hand tricer reset
with mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
) as hands:
    
    while True:
        #capture frame with useing camera
        frame = picam2.capture_array()

        # like mirror
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # hand detection
        results = hands.process(rgb_frame)

        gesture_result = "" # result text reset
        h, w, _ = frame.shape
        center_screen_x = w // 2

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # center of hand
                cx, cy = 0, 0
                for lm in hand_landmarks.landmark:
                    cx += lm.x
                    cy += lm.y
                cx /= len(hand_landmarks.landmark)
                cy /= len(hand_landmarks.landmark)

                center_x, center_y = int(cx * w), int(cy * h)

                offset_x = center_x - center_screen_x
                direction = "right" if offset_x > 0 else "left"
                print(f"hand center move {abs(offset_x)} pixel move {direction} move.")

                # center point (green)
                cv2.circle(frame, (center_x, center_y), 10, (0, 255, 0), -1)

                # how manyfinger
                
                tips = [8, 12, 16, 20] 
                fingers = []
                for tip in tips:
                    if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                total_fingers = sum(fingers)

                #gesture text setting
                if total_fingers == 4:
                    gesture_result = "1"
                elif total_fingers == 0:
                    gesture_result = "0"
                else:
                    gesture_result = "-"

                # show landmark
                for id, lm in enumerate(hand_landmarks.landmark):
                    x, y = int(lm.x * w), int(lm.y * h)
                    color = (0, 255, 0) if (x == center_x and center_y) else (0, 0, 255)
                    cv2.circle(frame, (x, y), 5, color, -1)
        
        else:
            print("hand isnt detected")
        
        #center circle
        cv2.circle(frame, (w // 2, h // 2), 8, (0, 0, 0), -1)
    
        # show gesture result
        cv2.putText(frame, f"Gesture: {gesture_result}", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

        # show result
        cv2.imshow("Hand Detection", frame)

        # if press 'q' stop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()



































