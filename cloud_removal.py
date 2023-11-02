import numpy as np
import matplotlib.pyplot as plt
# from matplotlib.colors import LogNorm

import file_selection

START, END = '01/01/2019', '01/03/2019'
# IR16, VIS8, VIS6 = file_selection.load_in_range('all', START, END)
VIS6 = file_selection.load_in_range('VIS6', START, END).astype(np.uint32)
# # colour = np.stack((IR16, VIS8, VIS6), axis=-1)

# IR16_central_pixel = IR16[:, 1856, 1856]
# VIS8_central_pixel = VIS8[:, 1856, 1856]
VIS6_central_pixel = VIS6[:, 1856, 1856]

# plt.plot(IR16_central_pixel, label="IR16")
# plt.plot(VIS8_central_pixel, label="VIS8")
plt.figure(figsize=(12, 9))
plt.plot(VIS6_central_pixel, label="VIS6 data")

p = 3  # power the reciprocal is raised to during weighting.
for window_size in (3, 5, 7, 9, 11):
    array = VIS6_central_pixel
    array_size = array.size
    rolling_average = []
    for i in range(array_size):
        window_start = i - (window_size - 1) // 2
        window_end = i + (window_size - 1) // 2
        if window_start < 0:
            window_start = 0
        if window_end > array_size:
            window_end = array_size
        in_window = array[window_start: window_end + 1]
        weighted_average = np.sum(in_window/in_window**p) / np.sum(1/in_window**p)
        rolling_average.append(weighted_average)

    plt.plot(rolling_average,
             label="Window size = {:d} images".format(window_size))

plt.title("Rolling weighted average (p={:d}) over pixel data, with varying window sizes".format(p))
plt.xlabel("Image number")
plt.ylabel("Pixel value")
plt.legend()
plt.show()
