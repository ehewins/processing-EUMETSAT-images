# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 12:44:22 2023

@author: suhail
"""



import file_selection
import numpy as np
import matplotlib.pyplot as plt
import cv2

Start = '01/01/2019'
End   = '14/01/2019'

R,G,B = file_selection.load_in_range('all', Start, End)


#%%

cloud_removed = []

clouds =[]

for i in range(len(R)):
    
    red   = R[i]
    blue  = B[i]
    green = G[i]
    
    #global threshold
    r_1 = cv2.inRange(red, 30,40)
    b_1 = cv2.inRange(blue, 110, 255)
    g_1 = cv2.inRange(green, 110, 255)
    
    #add all the threshold for the global threshold
    img_1 = cv2.add(r_1,g_1,b_1)
    
    #first segment, north pole, notable chnage in blue
    b_seg1 = blue[0:500,0:3712]
    blue1 = cv2.inRange(b_seg1, 45, 90)

    #add border
    added1 = cv2.copyMakeBorder(blue1, 0, 3212, 0, 0, cv2.BORDER_CONSTANT)

    #add segments to global threshold
    one = cv2.add(img_1,added1)
    
    clouds.append(one)

    #subtract cloud in each colour
    red_c   = cv2.subtract(red, one)
    green_c = cv2.subtract(green, one)
    blue_c  = cv2.subtract(blue, one)
    
    #create image
    col = np.stack((red_c,green_c,blue_c),axis=-1)
    
    
    #append to list
    cloud_removed.append(col)
