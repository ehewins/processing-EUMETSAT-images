import numpy as np
import matplotlib.pyplot as plt
# from matplotlib.colors import LogNorm

import file_selection


def weighted_time_average(window, p=4):
    """
    Compute a weighted average of pixel values across time (axis 0) for a
    sequence of several images, where lower pixel value are weighed far more
    strongly than higher ones. The weight of datapoint x is 1 / x**p.
    """
    # Depending on the power p, larger types may be needed
    if p < 0 or p > 5:
        raise ValueError("Power p must be in range 0 <= p <= 5")
    if p == 5:
        type_needed = np.uint64
    elif p >= 3:
        type_needed = np.uint32
    elif p == 2:
        type_needed = np.uint16
    else:
        type_needed = np.uint8

    window = window.astype(type_needed)
    weighted_avg = np.sum(window/window**p, axis=0) / \
        np.sum(1/window**p, axis=0)
    return weighted_avg


START, END = '01/01/2019', '07/01/2019'
colour = np.stack((file_selection.load_in_range('all', START, END)), axis=-1)

p = 4  # power the reciprocal is raised to during weighting.
window_size = 5  # number of images averaged over during rolling average
array = colour
array_size = array.shape[0]
rolling_average = np.empty((0, *array.shape[1:]))
for i in range(array_size):
    window_start = max(i - (window_size - 1) // 2, 0)
    window_end = min(i + (window_size - 1) // 2, array_size)
    in_window = array[window_start: window_end + 1]
    weighted_average = weighted_time_average(in_window, p)
    rolling_average = np.append(rolling_average, [weighted_average], axis=0)

# Display before/after of the image from the middle of the timespan
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
ax1.imshow(array[7])
# Must be uint8 to display image properly
ax2.imshow(rolling_average[7].astype(np.uint8))
for ax in (ax1, ax2):
    ax.set_axis_off()
ax1.set_title("Original image")
ax2.set_title("Rolling time average with window size {:d}".format(window_size))

plt.show()
