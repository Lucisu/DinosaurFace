import cv2
import numpy as np
import dlib
import numpy
import tkinter as tk
import pyautogui
import time
from mss import mss
import os
from imutils import face_utils
root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

old_hv = (-100,-100)

GAP = 10
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = 0
# the first 'press' causes a lag, so called on begin
pyautogui.press("up")

cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

def find_dino():
    with mss() as sct:
        sct.shot()
    img_rgb = cv2.imread('monitor-1.png')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    for filename in os.listdir(os.path.dirname(os.path.abspath(__file__)) +'/imgs'):
        if filename == "screenshots":
            continue
        template = cv2.imread(os.path.dirname(os.path.abspath(__file__)) + "/imgs/"+filename,0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
        threshold = 0.95
        loc = np.where( res >= threshold)
        if len(list(zip(*loc[::-1]))) == 1:
            return True
        time.sleep(0.8)
    return False

print("Wait to find dino...")
while not find_dino():
    pass
print("Finded!")
started = 5000
while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    if (started == 0):
        for face in faces:
            landmarks = predictor(gray, face)
            shape = face_utils.shape_to_np(landmarks)
            # more pretty with all points
            for (x, y) in shape:
                cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

            nose = (landmarks.part(30).x, landmarks.part(30).y)

            up_left = (landmarks.part(1).x, landmarks.part(1).y)
            down_left = (landmarks.part(2).x, landmarks.part(2).y)

            up_right = (landmarks.part(15).x, landmarks.part(15).y)
            down_right = (landmarks.part(14).x, landmarks.part(14).y)

            mid_top = ( nose[0], int((up_left[1] + up_right[1])/2))
            mid_down = ( nose[0], int((down_left[1] + down_right[1])/2))
            mid = (int(abs((mid_top[0] + mid_down[0])/2)), int(abs((mid_top[1] + mid_down[1])/2)))

            cv2.circle(frame, mid_top, 2, (0, 255, 0), -1)
            cv2.circle(frame, mid_down, 2, (0, 255, 0), -1)

            cv2.line(frame, mid_top, mid_down, (0, 255, 0), 2)

            cv2.circle(frame, mid, 2, (255, 0, 0), -1)
            cv2.circle(frame, nose, 3, (0, 0, 255), -1)

            pos = mid[1] - nose[1]
            if pos > 0 and abs(pos) > GAP:
                pyautogui.keyUp("down")
                pyautogui.press("up")
                time.sleep(0.001)
            elif pos < 0 and abs(pos) > GAP:
                pyautogui.keyDown("down")
                time.sleep(0.001)
            else:
                pyautogui.keyUp("down")

    else:
        cv2.putText(frame, "Click to focus chrome window... " + str(int(started/1000)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
        started -= 100
    cv2.imshow("Frame", frame)
    cv2.moveWindow("Frame", screen_width, screen_height)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
