# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 13:30:27 2023

@author: suhai
"""

import numpy as np
import matplotlib.pyplot as plt
import cv2


#get the file name of images
from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir('images') if isfile(join('images', f))]

#print(onlyfiles[0])

img = plt.imread('images/'+str(onlyfiles[0]))
n= np.size(onlyfiles)

image_list =[]
for i in range(n):
    img = plt.imread('images/'+str(onlyfiles[i]))
    image_list.append(img)
#%%

files = np.array_split(image_list,3)

Ir16 = files[0]
Vis6 = files[1]
Vis8 = files[2]

R = Ir16[0] #.astype(np.uint16)
G = Vis8[0] #.astype(np.uint16)
B = Vis6[0] #.astype(np.uint16)

col = np.stack((R,G,B),axis=-1)

#plt.imshow(col.astype(np.uint8))

#%%

ret, thresh = cv2.threshold(R, 120, 255, cv2.THRESH_BINARY)

ret1, thresh1 = cv2.threshold(B, 120, 255, cv2.THRESH_BINARY)

ret1, thresh2 = cv2.threshold(G, 120, 255, cv2.THRESH_BINARY)

img_first = cv2.add(thresh, thresh1, thresh2)



#segment first
R_seg = R[0:1500,0:3712]
ret, red1 = cv2.threshold(R_seg, 45, 255, cv2.THRESH_BINARY)

G_seg = G[0:1500,0:3712]
ret ,green1 = cv2.threshold(G_seg, 45, 255, cv2.THRESH_BINARY)

B_seg = B[0:1500,0:3712]
ret ,blue1 = cv2.threshold(B_seg, 45, 255, cv2.THRESH_BINARY)

mino = cv2.add(red1,green1,blue1)
added1 = cv2.copyMakeBorder(mino, 0, 2212, 0, 0, cv2.BORDER_CONSTANT)
image1 = cv2.add(img_first,added1)

plt.figure()
plt.imshow(img_first, cmap='gray')

plt.figure()
plt.imshow(col.astype(np.uint8))





#%%

#segment first
R_seg = R[0:300,0:3712]
ret, red1 = cv2.threshold(R_seg, 45, 255, cv2.THRESH_BINARY)

G_seg = G[0:300,0:3712]
ret ,green1 = cv2.threshold(G_seg, 45, 255, cv2.THRESH_BINARY)

B_seg = B[0:300,0:3712]
ret ,blue1 = cv2.threshold(B_seg, 45, 255, cv2.THRESH_BINARY)


#second segment
R_seg2 = R[0:1500,0:1200]
ret, red2 = cv2.threshold(R_seg2, 50, 255, cv2.THRESH_BINARY)

G_seg2 = G[0:1500,0:1200]
ret, green2 = cv2.threshold(G_seg2, 50, 255, cv2.THRESH_BINARY)

B_seg2 = B[0:1500,0:1200]
ret, blue2 = cv2.threshold(B_seg2, 50, 255, cv2.THRESH_BINARY)

#segment third
R_seg = R[300:450,0:3712]
ret, red3 = cv2.threshold(R_seg, 50, 255, cv2.THRESH_BINARY)

G_seg = G[300:450,0:3712]
ret ,green3 = cv2.threshold(G_seg, 55, 255, cv2.THRESH_BINARY)

B_seg = B[300:450,0:3712]
ret ,blue3 = cv2.threshold(B_seg, 55, 255, cv2.THRESH_BINARY)

#segment fourth
R_seg = R[450:900,0:3712]
ret, red3 = cv2.threshold(R_seg, 50, 255, cv2.THRESH_BINARY)

G_seg = G[450:900,0:3712]
ret ,green3 = cv2.threshold(G_seg, 55, 255, cv2.THRESH_BINARY)

B_seg = B[450:900,0:3712]
ret ,blue3 = cv2.threshold(B_seg, 55, 255, cv2.THRESH_BINARY)


mino = cv2.add(red1,green1,blue1)
sicko = cv2.add(red2,green2,blue2)
nicko = cv2.add(red3,green3,blue3)

added1 = cv2.copyMakeBorder(mino, 0, 3412, 0, 0, cv2.BORDER_CONSTANT)
added2 = cv2.copyMakeBorder(sicko, 0, 2212, 0, 2512, cv2.BORDER_CONSTANT)
added3 = cv2.copyMakeBorder(nicko, 300, 3262, 0, 0, cv2.BORDER_CONSTANT)


image1 = cv2.add(img_first,added1)
image2 = cv2.add(image1,added2)
image3 = cv2.add(image2,added3)

plt.figure()
plt.imshow(image3, cmap='gray')

plt.figure()
plt.imshow(col.astype(np.uint8))

#%%


r_diff = cv2.subtract(R,thresh)
g_diff = cv2.subtract(G,thresh1)
b_diff = cv2.subtract(B,thresh2)

diff = np.stack((thresh,thresh1,thresh2),axis=-1)

#diff = np.stack((r_diff,g_diff,b_diff),axis=-1)
plt.imshow(diff)


#%%


blur = cv2.blur(R,(5,5))
blur1 = cv2.blur(G,(5,5))
blur2 = cv2.blur(B,(5,5))

#plt.imshow(blur, cmap='gray')


ret, thresh = cv2.threshold(blur, 150, 255, cv2.THRESH_BINARY)

ret1, thresh1 = cv2.threshold(blur1, 110, 255, cv2.THRESH_BINARY)

ret1, thresh2 = cv2.threshold(blur2, 110, 255, cv2.THRESH_BINARY)

img_first = cv2.add(thresh, thresh1, thresh2)

plt.imshow(img_first, cmap='gray')
