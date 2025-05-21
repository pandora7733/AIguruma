import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands = 1,
            min_detection_confidence = 0.7,
            min_tracking_confidence = 0.7,
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.results = None

    def get_hand_center_x(self, frame):
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb)

        if self.results.multi_hand_landmarks:
            hand_landmarks = self.results.multi_hand_landmarks[0]
            cx = sum([lm.x for lm in hand_landmarks.landmark]) / len(hand_landmarks.landmark)
            center_x = int(cx * w)
            return center_x
        return None
    
    def draw_landmarks(self, frame):
        if self.results and self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_drawing.drawing_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                )

    def close(self):
        self.hands.close()
        
