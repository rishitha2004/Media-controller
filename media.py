import cv2
import mediapipe as mp
import pyautogui
import time

def count_fingers(lst):
    cnt=0

    thresh=(lst.landmark[0].y*100-lst.landmark[9].y*100)/2

    if(lst.landmark[5].y * 100 - lst.landmark[8].y * 100) >thresh:
        cnt+=1

    if (lst.landmark[9].y * 100 - lst.landmark[12].y * 100) > thresh:
        cnt += 1

    if (lst.landmark[13].y * 100 - lst.landmark[16].y * 100) > thresh:
        cnt += 1

    if (lst.landmark[17].y * 100 - lst.landmark[20].y * 100) > thresh:
        cnt += 1

    if (lst.landmark[5].y * 100 - lst.landmark[4].y * 100) > 5:
        cnt += 1


    return cnt

cam = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

start_init=False

prev=-1
while(True):
    end_time=time.time()
    ret, frame = cam.read()
    frame=cv2.flip(frame,1)

    res = hands.process(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))

    if res.multi_hand_landmarks:

        hand_keyPoints=res.multi_hand_landmarks[0]
        # print(count_fingers(hand_keyPoints))
        cnt = count_fingers(hand_keyPoints)
        if not(prev==cnt):
            if not(start_init):
                start_time=time.time()
                start_init=True
            elif(end_time-start_time)>0.4:
                if (cnt == 1):
                    pyautogui.press("space")
                elif (cnt == 2):
                    pyautogui.press("left")
                elif (cnt == 3):
                    pyautogui.press("right")
                #   mmmmmmelif (cnt == 4):
                #     pyautogui.press("m")
                # elif (cnt == 5):
                #     pyautogui.press("f8")
                # prev = cnt
                start_init=False

        mpDraw.draw_landmarks(frame,hand_keyPoints,mpHands.HAND_CONNECTIONS)

    cv2.imshow("Live",frame)
    if(cv2.waitKey(1)==27):
        cv2.destroyAllWindows()
        cam.release()
        break