import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui
import time

# Webcam setup
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Screen size
screen_width, screen_height = pyautogui.size()

# To avoid multiple clicks
last_click_time = 0
click_delay = 0.3  # seconds

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img)

    if hands:
        hand = hands[0]
        lmList = hand["lmList"]

        # 👆 Get finger states (Thumb, Index, Middle, Ring, Pinky)
        fingers = detector.fingersUp(hand)

        # Fingertip points
        x_index, y_index = lmList[8][0], lmList[8][1]
        x_thumb, y_thumb = lmList[4][0], lmList[4][1]
        x_middle, y_middle = lmList[12][0], lmList[12][1]
        x_ring, y_ring = lmList[16][0], lmList[16][1]
        x_pinky, y_pinky = lmList[20][0], lmList[20][1]

        # ---------------- Cursor Movement ----------------
        if fingers == [0, 1, 0, 0, 0]:  # Only index up
            cursor_x = screen_width / 640 * x_index
            cursor_y = screen_height / 480 * y_index
            pyautogui.moveTo(cursor_x, cursor_y)
            cv2.putText(img, "Move", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 2)

        else:
            # ---------------- Left Click (Thumb + Index) ----------------
            length, _, img = detector.findDistance((x_thumb, y_thumb), (x_index, y_index), img)
            if length < 40 and time.time() - last_click_time > click_delay:
                pyautogui.click()
                last_click_time = time.time()
                cv2.putText(img, "Left Click", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # ---------------- Right Click (Thumb + Middle) ----------------
            length_mid, _, img = detector.findDistance((x_thumb, y_thumb), (x_middle, y_middle), img)
            if length_mid < 40 and time.time() - last_click_time > click_delay:
                pyautogui.rightClick()
                last_click_time = time.time()
                cv2.putText(img, "Right Click", (50, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # ---------------- Scroll Down (Thumb + Ring) ----------------
            length_ring, _, img = detector.findDistance((x_thumb, y_thumb), (x_ring, y_ring), img)
            if length_ring < 40 and time.time() - last_click_time > click_delay:
                pyautogui.scroll(-300)  # scroll down
                last_click_time = time.time()
                cv2.putText(img, "Scroll Down", (50, 150),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

            # ---------------- Scroll Up (Thumb + Pinky) ----------------
            length_pinky, _, img = detector.findDistance((x_thumb, y_thumb), (x_pinky, y_pinky), img)
            if length_pinky < 40 and time.time() - last_click_time > click_delay:
                pyautogui.scroll(300)  # scroll up
                last_click_time = time.time()
                cv2.putText(img, "Scroll Up", (50, 200),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

    cv2.imshow("Virtual Mouse", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()