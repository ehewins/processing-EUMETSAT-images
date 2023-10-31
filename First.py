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

#channels stack images
blue  = Vis6[0:1]
green = Vis8[0:1]
red   = Ir16[0:1]

#stack each of the colours

colour =[]
for i in range(730):
    blue  = Vis6[i]
    green = Vis8[i]
    red   = Ir16[i]
    col = np.stack((red,green,blue),axis=-1)
    colour.append(col)
    

#colour = np.clip(colour, 40,220)

#show image
#plt.imshow((colour).astype(np.uint8))
#Works until here
#%%
import matplotlib.animation as animation

colour # some array of images
frames = [] # for storing the generated images
fig = plt.figure()

for i in range(10):
    frames.append([plt.imshow(colour[i],animated=True)])

ani = animation.ArtistAnimation(fig, colour[0:20], interval=50, blit=True,
                                repeat_delay=1000)
ani.save('movie1.mp4')
plt.show()
