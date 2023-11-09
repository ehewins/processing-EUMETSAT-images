import os
from datetime import datetime, timedelta

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import medfilt

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


def single_pixel_tests():
    """
    This function is used to test time-averaging methods on single pixels, so
    their results can be compared in graphs of pixel value vs. time.
    """
    # Load pixel data
    target_pixel = [1856, 1856]
    start, end = datetime(2019, 1, 1), datetime(2019, 2, 1)
    pixel_data = file_selection.load_datetimes_three_colour(start, end)[:, *target_pixel]
    # Figures setup
    fig, ((ax1), (ax2), (ax3), (ax4)) = plt.subplots(4, 1, figsize=(10, 14))
    # Show the variation in each wavelength during this time window
    for channel, label in enumerate(('1600 nm', '800 nm', '600 nm')):
        ax1.plot(pixel_data[:, channel], label=label)
    array = pixel_data[:, 2]  # Extract 600 nm data
    ax2.plot(array, label='600 nm data')
    ax3.plot(array, label='600 nm data')
    ax4.plot(array, label='600 nm data')
    for window_size in (3, 7, 11):
        rolling_average = []
        weighted_rolling_average = []
        for i in range(array.size):
            window_start = max(i - (window_size - 1) // 2, 0)
            window_end = min(i + (window_size - 1) // 2, array.size)
            in_window = array[window_start: window_end + 1]
            # Calculate a simple rolling average within the time window
            rolling_average.append(weighted_time_average(in_window, p=0))
            # Calculate a weighted rolling average within the time window
            weighted_rolling_average.append(weighted_time_average(in_window,
                                                                  p=4))
        ax2.plot(rolling_average, label=f"Window size {window_size}")
        ax3.plot(weighted_rolling_average, label=f"Window size {window_size}")
        # Apply a median filter within the time window
        ax4.plot(medfilt(array, window_size),
                 label=f"Window size {window_size}")

    for ax in (ax1, ax2, ax3, ax4):
        ax.set_xlabel("Image number")
        ax.set_ylabel("Pixel value")
        ax.legend(loc='upper center')
    plt.show()


RESULTS_DIR = 'cloud_free_images'

# # Define week-long time intervals to average over
# week_dates = []
# start_date = datetime(2019, 1, 1)
# end_date = datetime(2020, 1, 1)
# current_date = start_date
# while current_date < end_date:
#     week_dates.append(current_date)
#     current_date += timedelta(weeks=1)

for w in range(52):
    time_window = file_selection.load_by_week(week=w)
    weighted_average = weighted_time_average(time_window)
    plt.imsave(os.path.join(RESULTS_DIR, "week_{:d}.jpg".format(w)),
               weighted_average.astype(np.uint8))
    print("Saved image for week {:d}".format(w))
