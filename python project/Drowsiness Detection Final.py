import cv2
import numpy as np
import dlib
from imutils import face_utils
import winsound
import time
import os

cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


sleep = 0
drowsy = 0
active = 0
status=""
color=(0,0,0)

def compute(ptA,ptB):
    dist = np.linalg.norm(ptA - ptB)
    return dist


#a=36/42
#b=37/43
#c=38/44
#d=41/47
#e=40/46
#f=39/45
def blinked(a,b,c,d,e,f):
    up = compute(b,d) + compute(c,e)
    down = compute(a,f)
    ratio = up/(2.0*down)

    if(ratio>0.24):
        return 2
    elif(ratio>0.21 and ratio<=0.24):
        return 1
    else:
        return 0


while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)

    for face in faces:
        #face_frame = frame.copy()
        landmarks = predictor(gray, face)
        landmarks = face_utils.shape_to_np(landmarks)

        left_blink = blinked(landmarks[36],landmarks[37],landmarks[38], landmarks[41], landmarks[40], landmarks[39])
        right_blink = blinked(landmarks[42],landmarks[43],landmarks[44], landmarks[47], landmarks[46], landmarks[45])
        
        if(left_blink==0 or right_blink==0):
            sleep+=1
            drowsy=0
            active=0
            if(sleep>6):
                winsound.PlaySound("beep-04.wav", 0)
                status="SLEEPING!"
                color = (0,0,255)
        elif(left_blink==1 or right_blink==1):
            sleep=0
            active=0
            drowsy+=1
            if(drowsy>6):
                status="Drowsy"
                color = (0,0,0)
        else:
            drowsy=0
            sleep=0
            active+=1
            if(active>6):
                status="Active"
                color = (0,255,0)
        
        cv2.putText(frame, status, (100,100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color,3)

        #for n in range(0, 68):
        #    (x,y) = landmarks[n]
        #    cv2.circle(face_frame, (x, y), 1, (255, 255, 255), -1)

        cv2.imshow("Frame", frame)
        #cv2.imshow("Result of detector", face_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            os._exit(0)





