try:
    import cv2
except ImportError:
    raise ImportError("Missing required module 'cv2'. Install with: pip install opencv-python") from None
import time
import mediapipe as mp
import pyautogui

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

GESTURE_COOLDOWN = 1.0

def get_finger_states(landmarks):
    tips = [4, 8, 12, 16, 20]
    pips = [2, 6, 10, 14, 18]
    wrist_y = landmarks[0].y
    states = {}
    # Thumb: check if thumb tip is above wrist (thumb up) as a simple proxy
    states["thumb"] = landmarks[4].y < wrist_y - 0.03
    names = ["index", "middle", "ring", "pinky"]
    for i, name in enumerate(names, start=1):
        tip_y = landmarks[tips[i]].y
        pip_y = landmarks[pips[i]].y
        states[name] = tip_y < pip_y - 0.02
    return states

def recognize_gesture(states):
    extended = [states["thumb"], states["index"], states["middle"], states["ring"], states["pinky"]]
    others_extended = any([states["index"], states["middle"], states["ring"], states["pinky"]])
    if all(extended):
        return "open_palm"
    if not any(extended):
        return "fist"
    if states["thumb"] and not others_extended:
        return "thumbs_up"
    return None

def action_for_gesture(gesture, action_state):
    now = time.time()
    if gesture is None:
        return None
    last = action_state.get(gesture, 0)
    if now - last < GESTURE_COOLDOWN:
        return None
    action_state[gesture] = now
    if gesture == "thumbs_up":
        pyautogui.press('playpause')
        return "Play/Pause"
    if gesture == "open_palm":
        pyautogui.press('volumeup')
        return "Increase Volume"
    if gesture == "fist":
        pyautogui.press('volumedown')
        return "Decrease Volume"
    return None

def main():
    print("Hand Gesture Recognition Demo")
    print("Gestures:")
    print("- Thumbs up: Play/Pause")
    print("- Open palm: Increase Volume")
    print("- Fist: Decrease Volume")
    print("Press 'q' to quit")
    print("Make sure your media player is active for play/pause to work")
    print()

    cap = cv2.VideoCapture(0)
    with mp_hands.Hands(min_detection_confidence=0.6, min_tracking_confidence=0.5, max_num_hands=1) as hands:
        action_state = {}
        last_action_text = ""
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)
            gesture = None
            if results.multi_hand_landmarks:
                lm_list = results.multi_hand_landmarks[0].landmark
                states = get_finger_states(lm_list)
                gesture = recognize_gesture(states)
                mp_drawing.draw_landmarks(frame, results.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)
            action = action_for_gesture(gesture, action_state)
            if action:
                last_action_text = f"{gesture} -> {action}"
                print(f"Performed action: {action}")
            # overlay
            if gesture:
                cv2.putText(frame, f"Gesture: {gesture}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,0), 2)
            if last_action_text:
                cv2.putText(frame, f"Action: {last_action_text}", (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
            cv2.imshow("Hand Gesture Demo (press q to quit)", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()