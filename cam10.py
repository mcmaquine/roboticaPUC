import cv2
import numpy as np

def nothing(x):
    pass

cam=cv2.VideoCapture(0)

cv2.namedWindow("Tracking")
cv2.createTrackbar("LH", "Tracking", 0, 255, nothing)
cv2.createTrackbar("LS", "Tracking", 65, 255, nothing)
cv2.createTrackbar("LV", "Tracking", 0, 255, nothing)
cv2.createTrackbar("UH", "Tracking", 35, 255, nothing)
cv2.createTrackbar("US", "Tracking", 240, 255, nothing)
cv2.createTrackbar("UV", "Tracking", 255, 255, nothing)

kernel=np.ones((5,5),np.uint8)
while (True):
    _, frame=cam.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    rangomax=np.array([50,255,50])
    rangomin=np.array([0,51,0])
    l_h = cv2.getTrackbarPos("LH", "Tracking")
    l_s = cv2.getTrackbarPos("LS", "Tracking")
    l_v = cv2.getTrackbarPos("LV", "Tracking")

    u_h = cv2.getTrackbarPos("UH", "Tracking")
    u_s = cv2.getTrackbarPos("US", "Tracking")
    u_v = cv2.getTrackbarPos("UV", "Tracking")

    l_b = np.array([l_h, l_s, l_v])
    u_b = np.array([u_h, u_s, u_v])

    mascara = cv2.inRange(hsv, l_b, u_b)
   
    opening=cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel)
    x,y,w,h=cv2.boundingRect(opening)
    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
    cv2.circle(frame,(x+w//2,y+h//2),5,(0,0,255),-1)
    res = cv2.bitwise_and(frame, frame, mask=mascara)
    cv2.imshow('camera',frame)

    cv2.imshow('opening',opening)
    cv2.imshow("res", res)
    k=cv2.waitKey(1)&0xFF
    if k==27:
        break
cam.release()
cv2.destroyAllWindows()
