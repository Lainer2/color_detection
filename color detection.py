import os
import cv2
import numpy as np
from PIL import Image

def get_limits(color):
    c = np.uint8([[color]])
    hsvc = cv2.cvtColor(c,cv2.COLOR_BGR2HSV)#change RBG color To HSV

    lower_limit = hsvc[0][0][0] - 10, 100, 100
    upper_limit = hsvc[0][0][0] + 10, 255, 255 #Creating the color range we want to detect

    lower_limit = np.array(lower_limit, dtype=np.uint8)
    upper_limit = np.array(upper_limit, dtype=np.uint8) #Making a numpy array
                                                        #Use uint8 to limit data to the last byte of info(2^8 = 256), color range is 0-255

    return lower_limit, upper_limit

def main():
    capt = cv2.VideoCapture(0) #create an array with what the camera sees
    while True: #loop that updates the camera and positions of detected pictures
        ret, frame = capt.read()
        
        #yellow = [0,255, 255]
        yellow = [87 ,213, 222]
        hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_limit, upper_limit = get_limits(color=yellow)
        mask = cv2.inRange(hsv_image, lower_limit, upper_limit)#mask shows ONLY pixels within the range

        cv2.imshow("frame", mask) #this shows the image, switching mask out for frame would just show regular video

        if cv2.waitKey(1) & 0xFF == ord("l"):
            break
    capt.release()
    cv2.destroyAllWindows

if __name__ == "__main__":
    main()
