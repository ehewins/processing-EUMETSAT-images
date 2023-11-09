# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 17:22:11 2023

@author: suhai
"""


import file_selection
import numpy as np
import matplotlib.pyplot as plt
import cv2


R4 = []
G4 = []
B4 = []

#image for each of the week
#51 weeks in total

#code takes a while to run so you may want to lower 51 to 5 for quicker results
#for data for a month
for week in range(51):
    R, G, B = file_selection.load_by_week(week, separate=True)
    ocean = []

    #run a loop for all the images in each week
    for i in range(len(R)):

        red = R[i]
        blue = B[i]
        green = G[i]

        #global threshold
        r_1 = cv2.inRange(red, 5, 15)
        b_1 = cv2.inRange(blue,  5, 30)
        g_1 = cv2.inRange(green, 5, 30)

        # add all the threshold for the global threshold
        img_1 = cv2.add(r_1, g_1, b_1)
        
        #convert to binary
        one = np.array(img_1)/255
        ocean.append(one)

    R2 = []
    G2 = []
    B2 = []
    #Keep the pixel that are ocean pixels
    for i in range(len(R)):
        R1 = np.array(R[i])*np.array(ocean[i])
        G1 = np.array(G[i])*np.array(ocean[i])
        B1 = np.array(B[i])*np.array(ocean[i])

        R2.append(R1)
        G2.append(G1)
        B2.append(B1)

    #Find the average value of each of the pixels
    #for the week. Then add each colour it an array.
    R3 = np.array(R2)
    R3 = R3.astype(float)
    R3[R3 == 0] = np.nan
    means = np.nanmean(R3, axis=0)

    B3 = np.array(B2)
    B3 = B3.astype(float)
    B3[B3 == 0] = np.nan
    means1 = np.nanmean(B3, axis=0)

    G3 = np.array(B2)
    G3 = B3.astype(float)
    G3[G3 == 0] = np.nan
    means2 = np.nanmean(G3, axis=0)

    R4.append(means)
    G4.append(means1)
    B4.append(means2)

#%%
#rename
Infared = R4

#requires a lot of memory
coloured = np.stack((R4, G4, B4), axis=-1)

#%%
#save infared, coloured and difference in each of there folder if you choose to.

for i in range(51):
    In = Infared[i]
    plt.imshow(3*In.astype(np.uint8))
    #save in a folder called Infrared
    #plt.savefig('Infrared/Images' + str(i) + 'png')
    plt.close()

#%%

for i in range(51):
    co = coloured[i]
    plt.imshow(3*co.astype(np.uint8))
    #save in a folder called coloured
    #plt.savefig('Coloured/Images' + str(i) + 'png')
    plt.close()

#Difference between sucessive weeks in the infared
#%%
diffe = []
for i in range(51):
    diff = cv2.subtract(Infared[i+1], Infared[i])
    plt.imshow(diff.astype(np.uint8))
    #save in a folder called Difference
    #plt.savefig('Difference/Images' + str(i) + 'png')
    diffe.append(diff)
    plt.close()

#%%
fig, (ax2) = plt.subplots(1, 1 , figsize=(8,8))

ax2.imshow(Infared[4].astype(np.uint8), vmin=10, vmax=35)
ax2.set_axis_off()

plt.show()
plt.savefig('Infared')

#%%

fig, (ax1, ax2, ax3) = plt.subplots(1, 3 , figsize=(10,8))

ax1.imshow(diffe[3].astype(np.uint8))
ax1.set_axis_off()

ax2.imshow(diffe[4].astype(np.uint8))
ax2.set_axis_off()

ax3.imshow(diffe[5].astype(np.uint8))
ax3.set_axis_off()

plt.show()
plt.savefig('current_moving')


plt.subplots_adjust(wspace=0, hspace=0)


#%%

# graph the increase in ocean temperature per week over the year
# find the average of the earth temperature in each week, 
#plot a function of ocean temperature on this side of the earth 
#over time

means =[]


for i in range(51):
    qwerty = Infared[i]
    wq = np.nanmean(qwerty)
    means.append(wq)

#%%

#anomalous data, so is deleted to get a better graph.
niko = np.delete(means,37)

x=np.arange(0,50,1)
plt.plot(x,niko) 
plt.xlabel('Weeks')
plt.ylabel('Average pixel value')
plt.savefig('CHange_in_ocean_temp.png')





