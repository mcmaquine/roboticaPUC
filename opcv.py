from ctypes import sizeof
from pickletools import uint8
import cv2
import numpy as np

# mouse callback function
def mouse_callback(event,x,y,flags,param):
    global ix, iy, count
    if event == cv2.EVENT_LBUTTONDOWN:
        ix = x
        iy = y
    
    elif event == cv2.EVENT_LBUTTONUP:
        print("Start X:{} End X:{} Start Y:{} End Y:{}".format(ix, x, iy, y))
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        selected_img = np.zeros((y - iy, x - ix, 3), np.uint8)
        selected_img[:,:] = frame[iy:y, ix:x]
        cv2.imshow("Pixel Selecionados", selected_img)
        count = 0
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

        print("LH:{}\tUH:{}\nLS:{}\tUS:{}\nLV:{}\tUV:{}".format(LH, UH,\
            LS, US, LV, UV))

        


# To read image from disk, we use
# cv2.imread function, in below method,
cam = cv2.VideoCapture(0)

# To hold the window on screen, we use cv2.waitKey method
# Once it detected the close input, it will release the control
# To the next line
# First Parameter is for holding screen for specified milliseconds
# It should be positive integer. If 0 pass an parameter, then it will
# hold the screen until user close it.

while (True):

    notUsed , frame = cam.read()
 
    # Creating GUI window to display an image on screen
    # first Parameter is windows title (should be in string format)
    # Second Parameter is image array
    cv2.imshow("Video", frame )
    cv2.setMouseCallback("Video", mouse_callback )

    key = cv2.waitKey(1)&0xFF
    if key ==27:
        break
 
# It is for removing/deleting created GUI window from screen
# and memory
cam.release()
cv2.destroyAllWindows()

# Versoes anteriores
 #elif event == cv2.EVENT_LBUTTONUP:
  #      print("Start X:{} End X:{} Start Y:{} End Y:{}".format(ix, x, iy, y))
   #     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #    pixelHSV = np.zeros((1,3), np.int_)
     #   count = 0
  #      for i in range(ix, x+1):
   #         for j in range(iy, y+1):
    #            print(hsv[j,i])
     #           pixelHSV = pixelHSV + hsv[j,i]
      #          count += 1
        
      #  pixelHSV = pixelHSV/count
       # print("Media HSV")
        #print(pixelHSV.astype(int))
