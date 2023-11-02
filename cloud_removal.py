import numpy as np
import matplotlib.pyplot as plt
# from matplotlib.colors import LogNorm

import file_selection

START, END = '01/01/2019', '07/01/2019'
IR16, VIS8, VIS6 = file_selection.load_in_range('all', START, END)
# VIS6 = file_selection.load_in_range('VIS6', START, END).astype(np.uint32)
colour = np.stack((IR16, VIS8, VIS6), axis=-1).astype(np.uint32)

p = 4  # power the reciprocal is raised to during weighting.
window_size = 9  # number of images averaged over during rolling average
array = colour
array_size = array.shape[0]
rolling_average = np.empty((0, *array.shape[1:]))
for i in range(array_size):
    window_start = max(i - (window_size - 1) // 2, 0)
    window_end = min(i + (window_size - 1) // 2, array_size)
    in_window = array[window_start: window_end + 1]
    weighted_average = np.sum(in_window/in_window**p, axis=0) / \
        np.sum(1/in_window**p, axis=0)
    rolling_average = np.append(rolling_average, [weighted_average], axis=0)

# Display before/after of the image from the middle of the timespan
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
ax1.imshow(array[7].astype(np.uint8))
ax2.imshow(rolling_average[7].astype(np.uint8))
for ax in (ax1, ax2):
    ax.set_axis_off()
ax1.set_title("Original image")
ax2.set_title("Rolling time average with window size {:d}".format(window_size))

plt.show()
