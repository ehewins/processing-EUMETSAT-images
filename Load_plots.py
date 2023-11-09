# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 12:55:36 2023

@author: suhai
"""

#if module doesn't work, run module file
import cv2
import matplotlib.pyplot as plt
import numpy as np
import Load_clouds


week = 20

clouds, removed =  Load_clouds.clouds(week)

#%%

fig, (ax1, ax2) = plt.subplots(1, 2 , figsize=(10,8))

ax1.imshow(clouds[0],cmap='gray')
ax1.set_axis_off()

ax2.imshow(removed[0].astype(np.uint8))
ax2.set_axis_off()
plt.show()

plt.savefig('cloudsvsremoved.png')

#%%

import file_selection

week =20
#load files
R,G,B = file_selection.load_by_week(week, separate = True)
col = np.stack((R,G,B), axis=-1)
fig, (ax1) = plt.subplots(1, 1 , figsize=(10,8))

ax1.imshow(col[0])
ax1.set_axis_off()
plt.show()

plt.savefig('Earth')
