#!/usr/bin/env python
# coding: utf-8

# In[7]:


import cv2
from matplotlib import pyplot as plt
import imutils
import numpy as np
import easyocr
import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")


# In[10]:


# add check_out Time
def anpr_v4():
    check_in = input('\n\nPlease press A to open the gate and record your Plate Info:').lower()
    #
    # check_in 
    if check_in == 'a':
        #
        # record time say welcome
        time_in = datetime.now()#.strftime("%Y-%m-%d %H:%M:%S")
        print('\n\nWelcome you check in at:', time_in.strftime("%Y-%m-%d %H:%M:%S"))
        
        #
        # take a picture an record to localize the coordinates of the plate
        gray = cv2.cvtColor(cv2.imread('01_picture/image_02.jpeg'), cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5),0) 
        canny = cv2.Canny(blur, threshold1=30,threshold2=200)
        
        keypoints = cv2.findContours(canny.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
        contours = sorted(imutils.grab_contours(keypoints), key=cv2.contourArea, reverse=True)[:10]
        
        location = []
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 10, True) # approxPolyDP(input_curve, epsilon, closed) -> https://www.programcreek.com/python/example/89328/cv2.approxPolyDP
            if len(approx) == 4:
                location = approx
                break
                
        mask = np.zeros(gray.shape, dtype=np.uint8)

        cv2.drawContours(mask, [location], 0,255, -1)

        (x,y) = np.where(mask==255)
        (x1, y1) = (np.min(x), np.min(y))
        (x2, y2) = (np.max(x), np.max(y))
        cropped_image = gray[x1:x2, y1:y2]
        
        # read out the plate info
        result = easyocr.Reader(['en']).readtext(cropped_image)
        
        text_sum=[]
        for x in range(len(result)):
            text_sum.append(result[x][-2])    
        plate = ' '.join(text_sum)
        
        print('We record your Plate as:', plate)
        
        #
        # Check out
        check_out = input('Please type in your plate number to get ticket bill:').lower()
        
        if check_out == plate.lower():
            time_out = datetime.now()
            print('You check out at:', time_out.strftime("%Y-%m-%d %H:%M:%S"))
            visit_time = int((time_out - time_in).total_seconds())
            payment = visit_time * 0.09
            print('Your bill amounts to',round(payment,2),'€')
        else:
            print('bye bye')
        
        
    else:
        print('bye bye')


# In[11]:


anpr_v4()


# In[ ]:




