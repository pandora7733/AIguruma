from picamera2 import Picamera2
import time
import cv2
from hand_tracker import HandTracker
from servo_controller import ServoController

picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()
time.sleep(2)

hand_tracker = HandTracker()
servo_controller = ServoController()



try:
    while True:
        frame = picam2.capture_array()
        frame = cv2.flip(frame, 1)

        h, w, _ = frame.shape
        center_x_screen = w // 2
        hand_center_x = hand_tracker.get_hand_center(frame)

        if hand_center_x is not None:
            offset_x = hand_center_x - center_x_screen
            normalized_offset = max(-1.0, min(1.0, offset_x / 320))
            angle = 90 + (normalized_offset * 45)
            angle = max(45, min(135, angle))
            servo_controller.set_angle(angle)
            print(f"[Servo] hand center x: {hand_center_x}, offset: {offset_x}, drive angle: {angle:.1f}")
        else:
            servo_controller.stop()
            print("[Servo] hand is not detected - stop motor")

        cv2.circle(frame, (w // 2, h // 2), 8, (0, 0, 0), -1)
        cv2.putText(frame, "Press 'q' to Quit", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.imshow("Hand Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    hand_tracker.close()
    servo_controller.cleanup()
    cv2.destroyAllWindows() 
