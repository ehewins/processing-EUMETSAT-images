# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 17:06:07 2023

@author: suhail
"""
import file_selection
import numpy as np
import cv2



def clouds(week):
    
    """
    This function uses file_selection to load in the range of images.
    Then taking those image and perform thresholding to find clouds in each
    of the images and return data about the locations of the clouds.
    
    The function produce the coloured images with the clouds replace with
    the value zero showing as black.
    """

    #load files
    R,G,B = file_selection.load_by_week(week, separate = True)


    #empty array for data
    cloud_removed = []
    clouds =[]
    

    for i in range(len(R)):
        
        #loop each image
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
        blue2 = cv2.inRange(b_seg2, 80, 120)

        g_seg2 = green[3000:3712,0:3712]
        green2 = cv2.inRange(g_seg2, 80, 120)
    
        img_2 = cv2.add(blue2,green2)
    
        #add border to segments
        added1 = cv2.copyMakeBorder(blue1, 0, 3212, 0, 0, cv2.BORDER_CONSTANT)
        added2 = cv2.copyMakeBorder(img_2, 3000, 0, 0, 0, cv2.BORDER_CONSTANT)

        #add segments to global threshold
        one = cv2.add(img_1,added1)
        two = cv2.add(one,added2)
    
        clouds.append(two)

        #subtract cloud in each colour
        red_c   = cv2.subtract(red, two)
        green_c = cv2.subtract(green, two)
        blue_c  = cv2.subtract(blue, two)
    
        #create image
        col = np.stack((red_c,green_c,blue_c),axis=-1)
    
        #append to list
        cloud_removed.append(col)
    
    #convert to array
    cloud_removed1 = np.array(cloud_removed)
    clouds1 = np.array(clouds)

    clouds2 =[]

    #change max value 255 to 1.
    for i in range(len(clouds1)):
        img = clouds[i]
        img = np.array(img/img.max(),dtype=np.uint8)
        clouds2.append(img)
        
    clouds2 = np.array(clouds2)
    
    return clouds2 , cloud_removed1



def Load_clouds(start,end):
    
    """
    This function uses file_selection to load in the range of images.
    Then taking those image and perform thresholding to find clouds in each
    of the images and return data about the locations of the clouds.
    
    The function produce the coloured images with the clouds replace with
    the value zero showing as black.
    """

    #load files
    R,G,B = file_selection.load_datetimes_three_colour(start, end)

    #empty array for data
    cloud_removed = []
    clouds =[]
    

    for i in range(len(R)):
        
        #loop each image
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
        blue2 = cv2.inRange(b_seg2, 80, 120)

        g_seg2 = green[3000:3712,0:3712]
        green2 = cv2.inRange(g_seg2, 80, 120)
    
        img_2 = cv2.add(blue2,green2)
    
        #add border to segments
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
    
    #convert to array
    cloud_removed1 = np.array(cloud_removed)
    clouds1 = np.array(clouds)

    clouds2 =[]

    #change max value 255 to 1.
    for i in range(len(clouds1)):
        img = clouds[i]
        img = np.array(img/img.max(),dtype=np.uint8)
        clouds2.append(img)
        
    clouds2 = np.array(clouds2)
    
    return clouds2 , cloud_removed1
