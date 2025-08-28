import cv2
import mediapipe as mp
import numpy as np
import time
import keyboard
import pyautogui

class HandControl:

    def __init__(self, video_visible = 1, video_url=0, width =720, height = 420):
        self.video_visible = video_visible
        self.cap = cv2.VideoCapture(video_url)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.status = 'running' #'camera'

        self.prev_time = 0
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils

        # Control Volume
        self.last_action_time = 0
        self.action_cooldown = 1.5  # Second
        self.last_gesture_change = 0
        self.min_gesture_time = 0.5

        # Save the last Gesture
        self.last_detected_gesture = 'unknown'
        self.mode = 'media'
        self.mode_cooldown = 1.5
        self.mode_current_time = time.time()

        #mouse
        self.smoothing = 1.5
        self.screen_width, self.screen_height = pyautogui.size()
        self.mouse_x, self.mouse_y = self.screen_width // 2 , self.screen_height // 2

    def control(self, frame):
        key = cv2.waitKey(1) & 0xFF
        if key in [ord('x'), ord('q'), ord('X'), ord('Q'),193]:
            self.status = 'exit'
        if key == ord('n'):
            self.status = 'camera' if self.status == 'running' else 'running'
    
    def run(self):
        # To process one frame for each 2 (30fps => 15fps processed just)
        frame_skip = 2
        frame_count = 0

        with self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        ) as hands:
            while True:
                s, frame = self.cap.read()
                # frame_count += 1

                # if frame_count % frame_skip != 0:
                #     continue

                if not s:
                    print('Error, cannot open the Camera')
                    break
                frame = cv2.flip(frame, 1)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(rgb_frame)
                
                h, w, _ = frame.shape
                cv2.putText(frame, "Press Q,X : Exit | four fingers (without thumb): Toggle state - music/ mouse", (10, h - 20), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                
                # Calculate the time to the next gesture
                cooldown_left = max(0, self.action_cooldown - (time.time() - self.last_action_time))

                if self.status == 'running' :
                    if results.multi_hand_landmarks:
                        for hand_landmarks in results.multi_hand_landmarks:
                            self.mp_drawing.draw_landmarks(
                                frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                            )
                            
                            result = self.is_finger_extended(hand_landmarks)
                            gesture = self.detect_gestures(result)

                            # print(self.mode.upper())

                            if gesture == 'four' and ((time.time() - self.mode_current_time) > self.mode_cooldown):
                                self.mode = 'mouse' if  self.mode == 'media' else 'media'
                                self.mode_current_time = time.time()
                            
                            media = ''
                            if self.mode == 'media' :
                                media = self.media_control(gesture)
                            else:
                                media = self.mouse_control(hand_landmarks,  gesture)

                            cv2.putText(frame, f"Mode: {self.mode.upper()}", (w-300, 80), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 200), 2)

                            # Some information on Screen
                            cv2.putText(frame, f"Action: {media}", (w-300, 130), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 200), 2)
                            
                            if cooldown_left > 0:
                                cv2.putText(frame, f"Cooldown: {cooldown_left:.1f}s", (10, 120), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                            
                            cv2.putText(frame, f"Gesture: {gesture}", (10, 90), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                
                # Frame Rate
                fps = int(1 / (time.time() - self.prev_time + 1e-6))
                self.prev_time = time.time()
                cv2.putText(frame, f'FPS: {fps}', (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                if self.video_visible :
                    cv2.imshow('Hand Gesture Control', frame)

                self.control(frame)
                if self.status == 'exit':
                    break
            
        self.cap.release()
        cv2.destroyAllWindows()

    def is_finger_extended(self, hand_landmarks):
        result = []
        
        # Thumb
        thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
        thumb_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_MCP]
        
        # Detect the Thumb
        wrist = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
        thumb_extended = thumb_tip.x > thumb_mcp.x if wrist.x < 0.5 else thumb_tip.x < thumb_mcp.x
        result.append(1 if thumb_extended else 0)
        
        # Else 4 fingers
        for tip, pip in [
            (self.mp_hands.HandLandmark.INDEX_FINGER_TIP, self.mp_hands.HandLandmark.INDEX_FINGER_PIP),
            (self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP, self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP),
            (self.mp_hands.HandLandmark.RING_FINGER_TIP, self.mp_hands.HandLandmark.RING_FINGER_PIP),
            (self.mp_hands.HandLandmark.PINKY_TIP, self.mp_hands.HandLandmark.PINKY_PIP)
        ]:
            tip_y = hand_landmarks.landmark[tip].y
            pip_y = hand_landmarks.landmark[pip].y
            result.append(1 if tip_y < pip_y else 0)
        return result
    
    def detect_gestures(self, matrix):
        # Check if gesture is fixes
        current_time = time.time()
        if current_time - self.last_gesture_change < self.min_gesture_time:
            return self.last_detected_gesture
        
        # Known gesture
        gestures = {
            (0, 1, 0, 0, 0): 'index',       # ☝️
            (0, 1, 1, 0, 0): 'peace',       # ✌️
            (0, 0, 0, 0, 1): 'pinky',       # 🤙
            (1, 1, 1, 1, 1): 'hand',        # ✋
            (0, 1, 1, 1, 0): 'three',       # ☝️
            (0, 1, 1, 1, 1): 'four',        # 🖕
            (0, 1, 0, 0, 1): 'rock',        # 🤘

            # unused but known
            (0, 0, 0, 0, 0): 'closed',      # 🤛    
            (1, 0, 0, 0, 0): 'thumb',       # 👍
            (1, 0, 0, 0, 1): 'phone',       # 🤙
            (1, 1, 0, 0, 1): 'phone',       # 🤙
            (0, 0, 0, 1, 1): 'shaka',       # 🤙
            (1, 0, 0, 1, 1): 'spiderman',   # 🕷️
        }
        
        # Search for the gesture
        gesture_tuple = tuple(matrix)
        detected_gesture = gestures.get(gesture_tuple, 'unknown')
        
        # Update the last_detected_gesture time 
        if detected_gesture != self.last_detected_gesture:
            self.last_gesture_change = current_time
            self.last_detected_gesture = detected_gesture
        
        # if 
        return detected_gesture

    def media_control(self, gesture):
        try:
            current_time = time.time()
            cooldown_remaining = self.action_cooldown - (current_time - self.last_action_time)
            
            if cooldown_remaining > 0:
                return f"Cooldown: {cooldown_remaining:.1f}s"
            
            # Actions for each gesture
            actions = {
                'hand': ("play/pause media", "▶️⏸️"),
                'peace': ("next track", "⏭️"),
                'thumb': ("previous track", "⏮️"),
                'index': ("volume up", "🔊"),
                'pinky': ("volume down", "🔉"),
                'rock': ("volume mute", "🔇"),
            }
            
            if gesture in actions:
                key, emoji = actions[gesture]
                if key in ['volume up', 'volume down']:
                    for i in range(3):
                        keyboard.send(key)
                else:
                    keyboard.send(key)
                self.last_action_time = current_time
                return f"{emoji} {gesture}"
            
            return "Neutral"
        
        except Exception as e:
            print(f"Media control error: {e}")
            return "Error"

    def mouse_control(self, hand_landmarks,  gesture):

        if gesture == 'index':
            index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
            screen_y = np.interp(index_tip.y, [0.2, 0.8], [0, self.screen_height])
            screen_x = np.interp(index_tip.x, [0.2, 0.8], [0, self.screen_width])
            pyautogui.moveTo(screen_x, screen_y, duration= 0)
            self.mouse_x, self.mouse_y = screen_x, screen_y

            # target_x = np.interp(index_tip.x, [0.2, 0.8], [0, self.screen_width])
            # target_y = np.interp(index_tip.y, [0.2, 0.8], [0, self.screen_height])
            # self.mouse_x += (target_x - self.mouse_x) / self.smoothing
            # self.mouse_y += (target_y - self.mouse_y) / self.smoothing
            # pyautogui.moveTo(self.mouse_x, self.mouse_y, duration=0)
            return "Moving Mouse"
        
        current_time = time.time()
        if current_time - self.last_action_time < self.action_cooldown:
            cooldown_left = self.action_cooldown - (current_time - self.last_action_time)
            return f"Cooldown: {cooldown_left:.1f}s"

        if gesture == 'peace':
            pyautogui.click(button='left')
            self.last_action_time = time.time() 
            return "Left Click!"
        if gesture == 'three':
            pyautogui.click(button='right')
            self.last_action_time = time.time() 
            return "Right Click!"
        if gesture == 'closed':
            pyautogui.click(clicks=2, interval=0.1)
            self.last_action_time = time.time() 
            return "Double Click!"
        if gesture == 'hand':
            self.status = 'exit'
            return 'Done'
        
        self.last_detected_gesture = gesture
        
        return "Mouse Idle"


if __name__ == '__main__':
    video_visible = input('Do you want the camera to be visible (Y|N): ')
    video_visible = 0 if video_visible.lower() == 'n' else '1'
    app = HandControl(video_visible)
    try:
        app.run()
    except KeyboardInterrupt:
        print("Program interrupted by user")
    finally:
        cv2.destroyAllWindows()