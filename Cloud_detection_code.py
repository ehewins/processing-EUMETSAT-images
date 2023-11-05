# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 12:05:08 2023

@author: suhail
"""


#This detects most of the clouds and is pretty quick for 1 month.
# the list takes a while to load so I didn't try it for a year.

import file_selection
import numpy as np
import matplotlib.pyplot as plt
import cv2

Start = '01/01/2019'
End   = '28/01/2019'

R,G,B = file_selection.load_in_range('all', Start, End)


#%%

#empty array for the data
clouds=[]

cloud_removed = []

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


    ## segments
    #first segment, north pole, notable chnage in blue
    b_seg1 = blue[0:500,0:3712]
    blue1 = cv2.inRange(b_seg1, 45, 90)

    #second segment, south pole, notable change in blue and green
    b_seg2 = blue[3000:3712,0:3712]
    blue2 = cv2.inRange(b_seg2, 80, 255)

    g_seg2 = green[3000:3712,0:3712]
    green2 = cv2.inRange(g_seg2, 80, 255)
    
    img_2 = cv2.add(blue2,green2)

    #third segment, left side
    b_seg3 = blue[0:3712,0:1200]
    blue3 = cv2.inRange(b_seg3, 90, 255)

    g_seg3 = green[0:3712,0:1200]
    green3 = cv2.inRange(g_seg3, 90, 255)
    
    img_3 = cv2.add(blue3,green3)

    #fourth segment, right side
    b_seg4 = blue[0:3712,2512:3712]
    blue4 = cv2.inRange(b_seg4, 85, 255)


    #add borders to all the segments
    added1 = cv2.copyMakeBorder(blue1, 0, 3212, 0, 0, cv2.BORDER_CONSTANT)
    added2 = cv2.copyMakeBorder(img_2, 3000, 0, 0, 0, cv2.BORDER_CONSTANT)
    added3 = cv2.copyMakeBorder(img_3, 0, 0, 0, 2512, cv2.BORDER_CONSTANT)
    added4 = cv2.copyMakeBorder(blue4, 0, 0, 2512, 0, cv2.BORDER_CONSTANT)


    #could write this as one line of code, but I think it's clearer like this.
    #add all the segments together
    one = cv2.add(img_1,added1)
    two = cv2.add(one,added2)
    three = cv2.add(two,added3)
    four = cv2.add(three,added4)
    
    clouds.append(four)


    #subtract clouds
    red_c   = cv2.subtract(red,four)
    green_c = cv2.subtract(green,four)
    blue_c  = cv2.subtract(blue,four)
    
    #create image
    col = np.stack((red_c,green_c,blue_c),axis=-1)
    
    #append to list
    cloud_removed.append(col)
    
    
#%%

#list of clouds
#plt.figure()
#plt.imshow(clouds[],cmap='gray)

#images with the clouds removed
#plt.figure()
#plt.imshow(clouds[], cmap='gray')


