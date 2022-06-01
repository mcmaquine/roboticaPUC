#   Autor: Matheus Maquiné
#   Finalidade: Trabalho Final na disciplina de Robótica Industrial
#   O arquivo fonte original contém comentários por todo o programa

import cv2
import numpy as np

def nothing(x):
    pass

selecting = False

cam=cv2.VideoCapture(0)
_, frame=cam.read()

cv2.namedWindow("Tracking")
cv2.createTrackbar("LH", "Tracking", 0, 255, nothing)
cv2.createTrackbar("LS", "Tracking", 65, 255, nothing)
cv2.createTrackbar("LV", "Tracking", 0, 255, nothing)
cv2.createTrackbar("UH", "Tracking", 35, 255, nothing)
cv2.createTrackbar("US", "Tracking", 240, 255, nothing)
cv2.createTrackbar("UV", "Tracking", 255, 255, nothing)

# mouse callback function
def mouse_callback(event,x,y,flags,param):
    global ix, iy, selecting
    if event == cv2.EVENT_LBUTTONDOWN:
        selecting = True
        ix = x
        iy = y
    
    elif event == cv2.EVENT_LBUTTONUP:
        selecting = False
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        selected_img = np.zeros((y - iy, x - ix, 3), np.uint8)
        selected_img[:,:] = frame[iy:y, ix:x]
        h = []
        s = []
        v = []

        for i in range(ix, x+1):
            for j in range(iy, y+1):
                h.append( hsv[j,i][0] )
                s.append( hsv[j,i][1] )
                v.append( hsv[j,i][2] )
            
        LH = min(h)
        UH = max(h)
        LS = min(s)
        US = max(s)
        LV = min(v)
        UV = max(v)

        cv2.setTrackbarPos("LH", "Tracking", LH)
        cv2.setTrackbarPos("UH", "Tracking", UH)
        cv2.setTrackbarPos("LS", "Tracking", LS)
        cv2.setTrackbarPos("US", "Tracking", US)
        cv2.setTrackbarPos("LV", "Tracking", LV)
        cv2.setTrackbarPos("UV", "Tracking", UV)

kernel=np.ones((5,5),np.uint8)
while (True):

    if selecting == False:
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

    if selecting == False:
        mascara = cv2.inRange(hsv, l_b, u_b)
        opening=cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel)
        x,y,w,h=cv2.boundingRect(opening)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
        cv2.circle(frame,(x+w//2,y+h//2),5,(0,0,255),-1)
        res = cv2.bitwise_and(frame, frame, mask=mascara)
    
    cv2.imshow("camera",frame)
    cv2.setMouseCallback("camera", mouse_callback )

    if selecting == False:
        cv2.imshow('opening',opening)
        cv2.imshow("res", res)
    
    k=cv2.waitKey(1)&0xFF
    if k==27:
        break
cam.release()
cv2.destroyAllWindows()
