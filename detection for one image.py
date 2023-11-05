# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 13:22:46 2023

@author: suhai
"""

import file_selection
import numpy as np
import matplotlib.pyplot as plt
import cv2

Start = '01/01/2019'
End   = '03/01/2019'

R,G,B = file_selection.load_in_range('all', Start, End)

#plt.figure()
#plt.imshow(Ir16[0])
#plt.figure()
#plt.imshow(Vis8[0])
#plt.figure()
#plt.imshow(Vis6[0])


col = np.stack((R[0],G[0],B[0]),axis=-1)

plt.imshow(col)


#%%

blur = cv2.GaussianBlur(R[0],(5,5),0)
blur1 = cv2.GaussianBlur(G[0],(5,5),0)
blur2 = cv2.GaussianBlur(B[0],(5,5),0)

#global threshold
rr = cv2.inRange(blur, 30,40)
br = cv2.inRange(blur1, 110, 255)
gr = cv2.inRange(blur2, 110, 255)

img_first = cv2.add(rr,br,gr)

plt.imshow(img_first)

#segment first
B_seg = blur2[0:500,0:3712]
blue = cv2.inRange(B_seg, 45, 90)


#second segment
B_seg1 = blur2[3000:3712,0:3712]
blue1 = cv2.inRange(B_seg1, 80, 255)

G_seg1 = blur1[3000:3712,0:3712]
green1 = cv2.inRange(G_seg1, 80, 255)

#third segment

B_seg2 = blur2[0:3712,0:1200]
blue2 = cv2.inRange(B_seg2, 90, 255)

G_seg2 = blur1[0:3712,0:1200]
green2 = cv2.inRange(G_seg2, 90, 255)

#fourth segment

B_seg3 = blur2[0:3712,2512:3712]
blue3 = cv2.inRange(B_seg3, 85, 255)

#G_seg3 = blur2[0:3712,2512:3712]
#green3 = cv2.inRange(G_seg3, 90, 255)

#plt.imshow(blue3)



ninko = cv2.add(blue1,green1)

finko = cv2.add(blue2,green2)



added1 = cv2.copyMakeBorder(blue, 0, 3212, 0, 0, cv2.BORDER_CONSTANT)

added2 = cv2.copyMakeBorder(ninko, 3000, 0, 0, 0, cv2.BORDER_CONSTANT)

added3 = cv2.copyMakeBorder(finko, 0, 0, 0, 2512, cv2.BORDER_CONSTANT)

added4 = cv2.copyMakeBorder(blue3, 0, 0, 2512, 0, cv2.BORDER_CONSTANT)



image1 = cv2.add(img_first,added1)

image2 = cv2.add(image1,added2)

image3= cv2.add(image2,added3)

image4= cv2.add(image3,added4)

#plt.figure()
#plt.imshow(image4, cmap='gray')

#plt.figure()
#plt.imshow(col.astype(np.uint8))

kernel = np.ones((5,5),np.uint8)

image2 = cv2.dilate(image2,kernel,iterations = 1)




red   = cv2.subtract(R[0],image4)
green = cv2.subtract(G[0],image4)
blue  = cv2.subtract(B[0],image4)

col = np.stack((red,green,blue),axis=-1)
plt.figure()
plt.imshow(col)

#%%










