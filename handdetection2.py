
from picamera2 import Picamera2
import time
import cv2
import mediapipe as mp
import RPi.GPIO as GPIO

# settings mediaPipe
mp_hands = mp.solutions.hands

# settings Picamera2
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()
time.sleep(2) # wait camera safe

SERVO_PIN = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setup(SERVO_PIN, GPIO.OUT)
servo = GPIO.PWM(SERVO_PIN, 50) #50hz
servo.start(0)

def setServoAngle(angle):
    duty = 2.5 + (angle / 180.0) * 10 # 0 angle = 2.5, 180 angle = 12.5
    servo.ChangeDutyCycle(duty)



# MediaPipe hand tricer reset
with mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
) as hands:
    
    try:
        while True:
            #capture frame with useing camera
            frame = picam2.capture_array()

            # like mirror
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # hand detection
            results = hands.process(rgb_frame)

            h, w, _ = frame.shape
            center_x_screen = w // 2

            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]
                
                cx = sum([lm.x for lm in hand_landmarks.landmark] / len(hand_landmarks.landmark))
                center_x = int(cx * w)

                offset_x = center_x - center_x_screen
                normalized_offset = max(-1.0, min(1.0, offset_x / 320))

                angle = 90 + (normalized_offset * 45)
                angle = max(45, min(135, angle))

                setServoAngle(angle)
                print(f"[Servo] hand center x: {center_x}, offset: {offset_x}, driveangle: {angle:.1f}")

            else:
                servo.ChangeDutyCycle(0)
                print("hand isnt detected -> stop moter")
            
            #center circle
            cv2.circle(frame, (w // 2, h // 2), 8, (0, 0, 0), -1)
        
            # show gesture result
            cv2.putText(frame, "Press 'q' to Quit", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # show result
            cv2.imshow("Hand Tracking", frame)

            # if press 'q' stop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        servo.stop()
        GPIO.cleanup()            
        cv2.destroyAllWindows()



































