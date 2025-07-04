import cv2
import mediapipe as mp
import pyautogui
import time
import math
import webbrowser

from actions import (
    perform_middle_finger_action,
    perform_ring_finger_action,
    perform_little_finger_action,
)

# Setup
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)
screen_width, screen_height = pyautogui.size()

# Track gesture state
prev_gesture = None
last_action_time = 0

# === GESTURE DETECTORS ===
def count_extended_fingers(landmarks):
    fingers = []
    # Thumb
    fingers.append(landmarks[4].x < landmarks[3].x)
    # Other fingers
    fingers += [landmarks[i].y < landmarks[i - 2].y for i in [8, 12, 16, 20]]
    return sum(fingers)

def is_open_hand(landmarks): return count_extended_fingers(landmarks) == 5
def is_fist(landmarks): return count_extended_fingers(landmarks) == 0
def is_pointing_index(landmarks): return count_extended_fingers(landmarks) == 1
def is_peace_sign(landmarks): return landmarks[8].y < landmarks[6].y and landmarks[12].y < landmarks[10].y and all(landmarks[i].y > landmarks[i - 2].y for i in [16, 20])
def is_three_fingers(landmarks): return count_extended_fingers(landmarks) == 3

def is_middle_finger(landmarks):
    return (landmarks[12].y < landmarks[10].y and  # Middle finger up
            landmarks[8].y > landmarks[6].y and    # Index down
            landmarks[16].y > landmarks[14].y and  # Ring down
            landmarks[20].y > landmarks[18].y)     # Little down

def is_ring_finger(landmarks):
    return (landmarks[16].y < landmarks[14].y and  # Ring finger up
            landmarks[8].y > landmarks[6].y and    # Index down
            landmarks[12].y > landmarks[10].y and  # Middle down
            landmarks[20].y > landmarks[18].y)     # Little down

def is_little_finger(landmarks):
    return (landmarks[20].y < landmarks[18].y and  # Little finger up
            landmarks[8].y > landmarks[6].y and    # Index down
            landmarks[12].y > landmarks[10].y and  # Middle down
            landmarks[16].y > landmarks[14].y)     # Ring down

def is_click(landmarks):
    dist = math.hypot(landmarks[4].x - landmarks[8].x, landmarks[4].y - landmarks[8].y)
    return dist < 0.05

def move_mouse(landmarks, frame_shape):
    x, y = int(landmarks[8].x * frame_shape[1]), int(landmarks[8].y * frame_shape[0])
    pyautogui.moveTo(x * screen_width / frame_shape[1], y * screen_height / frame_shape[0], duration=0.01)

# === ACTIONS ===
def open_youtube():
    webbrowser.open("https://www.youtube.com")

def play_pause():
    pyautogui.press("space")

def mouse_click():
    pyautogui.click()

def volume_up(): pyautogui.press("volumeup")
def volume_down(): pyautogui.press("volumedown")

def switch_app(): pyautogui.hotkey("alt", "tab")

# === MAIN LOOP ===    
with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                landmarks = hand_landmarks.landmark
                now = time.time()

                if is_open_hand(landmarks) and prev_gesture != "open":
                    if now - last_action_time > 2:
                        open_youtube()
                        prev_gesture = "open"
                        last_action_time = now

                elif is_fist(landmarks) and prev_gesture != "fist":
                    if now - last_action_time > 1:
                        play_pause()
                        prev_gesture = "fist"
                        last_action_time = now

                elif is_pointing_index(landmarks):
                    move_mouse(landmarks, frame.shape)
                    if is_click(landmarks) and now - last_action_time > 1:
                        mouse_click()
                        last_action_time = now
                    prev_gesture = "pointing"

                elif is_peace_sign(landmarks) and prev_gesture != "peace":
                    if now - last_action_time > 1:
                        volume_up()  # or volume_down()
                        prev_gesture = "peace"
                        last_action_time = now

                elif is_three_fingers(landmarks) and prev_gesture != "switch":
                    if now - last_action_time > 1:
                        switch_app()
                        prev_gesture = "switch"
                        last_action_time = now

                elif is_middle_finger(landmarks) and prev_gesture != "middle":
                    if now - last_action_time > 2:
                        perform_middle_finger_action()
                        prev_gesture = "middle"
                        last_action_time = now

                elif is_ring_finger(landmarks) and prev_gesture != "ring":
                    if now - last_action_time > 2:
                        perform_ring_finger_action()
                        prev_gesture = "ring"
                        last_action_time = now

                elif is_little_finger(landmarks) and prev_gesture != "little":
                    if now - last_action_time > 2:
                        perform_little_finger_action()
                        prev_gesture = "little"
                        last_action_time = now

                else:
                    prev_gesture = None

        cv2.imshow("Gesture Controller", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break 

cap.release()
cv2.destroyAllWindows()
