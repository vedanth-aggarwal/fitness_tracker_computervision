import cv2
import numpy as np 
import time 
import mediapipe as mp
import module as m

cap = cv2.VideoCapture(0)
#img = cv2.imread("data/image.jpg")
detector = m.poseDetector()
count = 0
dir = 0 # 0 to 100 and 100 to 0
pTime = 0
while True:
    #success,img = cap.read()
    _,img = cap.read()
    #reimread("data/image.jpg")
    img = cv2.resize(img,(1280,720))
    img = detector.findPose(img,False)
    lmlist = detector.findPosition(img,False)
    if len(lmlist) != 0:
        # Right -> 12,14,25
        angle = detector.findAngle(img,11,13,15,True)
        #print(detector) # ANGLE IS REFLEX - CHANGE IT
        per = np.interp(angle,(210,310),(0,100))
        bar = np.interp(angle,(220,310),(650,100))
        # Check for dumbell curls
        color = (255, 0, 255)
        if per == 100:
            color = (0, 255, 0)
            if dir == 0:
                count += 0.5
                dir = 1
        if per == 0:
            color = (0, 255, 0)
            if dir == 1:
                count += 0.5
                dir = 0
        
        cv2.rectangle(img,(1100,100),(1175,650),color,3)
        cv2.rectangle(img,(1100,(int(bar))),(1175,650),color,cv2.FILLED)
        cv2.putText(img,f'{int(per)}%',(1100,75),cv2.FONT_HERSHEY_PLAIN,4,color,4)

        cv2.rectangle(img,(0,450),(250,720),(0,255,0),cv2.FILLED)
        cv2.putText(img,str(int(count)),(45,670),cv2.FONT_HERSHEY_PLAIN,10,(255,0,0),5)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img,str(int(fps)),(50,100),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),5)
        

    cv2.imshow('Image',img)
    cv2.waitKey(1)