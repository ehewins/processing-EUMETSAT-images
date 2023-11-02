# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 10:38:01 2023

@author: suhai
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 10:21:25 2023

@author: suhail
"""

import numpy as np
import matplotlib.pyplot as plt
import cv2
#from PIL import Image
#import glob

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
#%%

img_1 = Ir16[0]

plt.imshow(img_1,cmap='gray')



#%%

clouds = Ir16[0] - Ir16[1]

plt.imshow(clouds, cmap='gray')

#%%

R = Ir16[0] #.astype(np.uint16)
G = Vis8[0] #.astype(np.uint16)
B = Vis6[0] #.astype(np.uint16)

#I = (R+G+B)/3

#theta = ((R-G)+(R-B))/(2*(np.sqrt((R-G)**2 + (R-B)(G-B))))

#H = []

#if G>=B:

#S = 1 -()


col = np.stack((R,G,B),axis=-1)

plt.imshow(col.astype(np.uint8))

#%%
#from matplotlib.colors import LogNorm

#top = ( R - (B + G))

#bottom = (R + B + G)

#N = top / bottom



#plt.imshow(N,cmap='gray',norm =LogNorm())



#plt.imshow()


#%%

binary = cv2.threshold(R, 150, 255, cv2.THRESH_BINARY)

binary1 = cv2.threshold(B, 110, 255, cv2.THRESH_BINARY)

binary2 = cv2.threshold(G, 110, 255, cv2.THRESH_BINARY)


plt.imshow(binary[1])
plt.figure()
plt.imshow(binary1[1])
plt.figure()
plt.imshow(binary2[1])

#%%
#thresh1 = cv2.adaptiveThreshold(B, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                          #cv2.THRESH_BINARY, 205, 1) 

#tot = binary[1] +binary1[1]+ binary2[1]

#plt.imshow(tot)

#col = (R+G+B)

#diff = col-tot

#plt.imshow(col)


#%% 


binary = cv2.threshold(R, 150, 255, cv2.THRESH_BINARY)

binary1 = cv2.threshold(B, 110, 255, cv2.THRESH_BINARY)

binary2 = cv2.threshold(G, 110, 255, cv2.THRESH_BINARY)

#colr = np.stack((binary[1],binary1[1],binary2[1]),axis =-1)

vis = cv2.add(binary[1],binary1[1],binary2[1])

#plt.imshow(colr)

#diff = cv2.subtract(col,colr)

#for i in range(3712):
 #   for j in range(3712):
  #      ni = vis[i,j] 
   #     if ni == 255:
    #        col[i,j] =0
        
        
#transparancy by using four colour channels
        

        



plt.imshow(vis, cmap = 'gray')

#k-mean cv2 to segment the image then using a mask to remove the clouds from the original image
#sciklit super pixel SLIC


#%%

R_s = R[0:1500,0:3712]

binary = cv2.threshold(R_s, 90, 255, cv2.THRESH_BINARY)
#plt.figure()
#plt.imshow(binary[1],cmap='gray')
#plt.figure()
#plt.imshow(R_s,cmap='gray')


G_s = G[0:1500,0:3712]

binary1 = cv2.threshold(G_s, 100, 255, cv2.THRESH_BINARY)

plt.figure()
plt.imshow(binary1[1],cmap='gray')
plt.figure()
plt.imshow(G_s,cmap='gray')

B_s = B[450:900,0:3712]

binary2 = cv2.threshold(B_s, 80, 255, cv2.THRESH_BINARY)

#plt.figure()
#plt.imshow(binary2[1],cmap='gray')
#plt.figure()
#plt.imshow(B_s,cmap='gray')

#%%


vis1 = cv2.add(binary[1],binary1[1],binary2[1])
#plt.imshow(vis, cmap = 'gray')

image = cv2.copyMakeBorder(vis1, 0, 3112, 0, 0, cv2.BORDER_CONSTANT)

plt.imshow(image, cmap='gray')

#%%

comb = cv2.add(vis,image)

plt.imshow(comb, cmap='gray')

plt.figure()

plt.imshow(col.astype(np.uint8))




#%%

R_s1 = R[0:1500,0:1200]

binary = cv2.threshold(R_s1, 50, 255, cv2.THRESH_BINARY)

#plt.figure()
#plt.imshow(binary[1],cmap='gray')
#plt.figure()
#plt.imshow(R_s1,cmap='gray')

G_s1 = G[0:1500,0:1200]

binary1 = cv2.threshold(G_s1, 50, 255, cv2.THRESH_BINARY)

#plt.figure()
#plt.imshow(binary1[1],cmap='gray')
#plt.figure()
#plt.imshow(G_s1,cmap='gray')

B_s1 = B[0:1500,0:1200]

binary2 = cv2.threshold(B_s1, 50, 255, cv2.THRESH_BINARY)

plt.figure()
plt.imshow(binary2[1],cmap='gray')
plt.figure()
plt.imshow(B_s1,cmap='gray')



#%%


vis2 = cv2.add(binary[1],binary1[1],binary2[1])
plt.figure()
plt.imshow(vis2, cmap = 'gray')

image1 = cv2.copyMakeBorder(vis2, 600, 2212, 0, 2512, cv2.BORDER_CONSTANT)

plt.figure()
plt.imshow(image1, cmap='gray')

#%%

tomb = cv2.add(comb,image1)

plt.imshow(tomb, cmap='gray')

plt.figure()

plt.imshow(col.astype(np.uint8))


#%%

R_s2 = R[650:850,1200:1420]

binary = cv2.threshold(R_s2, 40, 100, cv2.THRESH_BINARY)

#40 to 100

#plt.figure()
#plt.imshow(binary[1],cmap='gray')
#plt.figure()
#plt.imshow(R_s2,cmap='gray')

G_s2 = G[650:850,1200:1420]

binary1 = cv2.threshold(G_s2, 40, 100, cv2.THRESH_BINARY)


#.figure()
#plt.imshow(binary1[1],cmap='gray')
#plt.figure()
#plt.imshow(G_s2,cmap='gray')

B_s2 = B[650:850,1200:1420]

binary2 = cv2.threshold(B_s2, 40, 100, cv2.THRESH_BINARY)

plt.figure()
plt.imshow(binary2[1],cmap='gray')
plt.figure()
plt.imshow(B_s2,cmap='gray')







#%%


vis2 = cv2.add(binary[1],binary1[1],binary2[1])
plt.figure()
plt.imshow(vis2, cmap = 'gray')

image1 = cv2.copyMakeBorder(vis2, 600, 2212, 1200, 1512, cv2.BORDER_CONSTANT)

plt.figure()
plt.imshow(image1, cmap='gray')

#%%

tomb = cv2.add(comb,image1)

plt.imshow(tomb, cmap='gray')

plt.figure()

plt.imshow(col.astype(np.uint8))
