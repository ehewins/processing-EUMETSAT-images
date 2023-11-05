# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 12:44:22 2023

@author: suhail
"""

#For day 22/09/2019, there is no image for red
#code doesn't work for that day. 


import file_selection
import numpy as np
import matplotlib.pyplot as plt
import cv2

Start = '23/10/2019'
End   = '23/11/2019'

R,G,B = file_selection.load_in_range('all', Start, End)




#%%

cloud_removed = []

clouds =[]

for i in range(len(R)):
    
    red   = R[i]
    blue  = B[i]
    green = G[i]
    
    #global threshold
    b_1 = cv2.inRange(blue, 120, 255)
    g_1 = cv2.inRange(green, 120, 255)
    
    #add all the threshold for the global threshold
    img_1 = cv2.add(g_1,b_1)
    
    #first segment, north pole, notable change in blue
    b_seg1 = blue[0:500,0:3712]
    blue1 = cv2.inRange(b_seg1, 55, 120)
    
    #second segment, south pole, notable change in blue and green
    b_seg2 = blue[3000:3712,0:3712]
    blue2 = cv2.inRange(b_seg2, 80, 255)

    g_seg2 = green[3000:3712,0:3712]
    green2 = cv2.inRange(g_seg2, 80, 255)
    
    img_2 = cv2.add(blue2,green2)
    
    #add border
    added1 = cv2.copyMakeBorder(blue1, 0, 3212, 0, 0, cv2.BORDER_CONSTANT)
    added2 = cv2.copyMakeBorder(img_2, 3000, 0, 0, 0, cv2.BORDER_CONSTANT)

    #add segments to global threshold
    one = cv2.add(img_1,added1)
    two = cv2.add(one,added2)
    
    clouds.append(one)

    #subtract cloud in each colour
    red_c   = cv2.subtract(red, two)
    green_c = cv2.subtract(green, two)
    blue_c  = cv2.subtract(blue, two)
    
    #create image
    col = np.stack((red_c,green_c,blue_c),axis=-1)
    
    
    #append to list
    cloud_removed.append(col)
    
#%%
#convert to array
cloud_removed1 = np.array(cloud_removed)
clouds1 = np.array(clouds)


clouds2 =[]

for i in range(len(clouds)):
    img = clouds[i]
    img = np.array(img/img.max(),dtype=np.uint8)
    clouds2.append(img)

#plt.figure()
#plt.imshow(cloud_removed[0])

#col = np.stack((R[0],G[0],B[0]),axis=-1)
#plt.figure()
#plt.imshow(col)
