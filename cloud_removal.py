import os
from datetime import datetime, timedelta

import numpy as np
import matplotlib.pyplot as plt

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


RESULTS_DIR = 'cloud_free_images'

# Define week-long time intervals to average over
week_dates = []
start_date = datetime(2019, 1, 1)
end_date = datetime(2020, 1, 1)
current_date = start_date
while current_date < end_date:
    week_dates.append(current_date)
    current_date += timedelta(weeks=1)

for w in range(len(week_dates) - 1):
    time_window = file_selection.load_datetimes_three_colour(week_dates[w],
                                                             week_dates[w + 1])
    weighted_average = weighted_time_average(time_window)
    plt.imsave(os.path.join(RESULTS_DIR, "week_{:d}.png".format(w)),
               weighted_average.astype(np.uint8))
    print("Saved image for week {:d}".format(w))
