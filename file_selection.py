"""
This program loads which files for the data analysis process to use.
"""

import os
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

IMAGE_DIR = 'images'
MIN_DATE = datetime(2019, 1, 1, 0, 0, 0)
MAX_DATE = datetime(2020, 1, 1, 23, 59, 59)


def load_in_range(wavelength='all', start='01/01/2019', end='01/01/2020'):
    """
    This function is used to load files from a specific range of dates, in a
    specific wavelength. Returns an array of images. If wavelength == 'all',
    three arrays will be returned in order of decreasing wavelength.

    The variable 'wavelength' must be one of ['all', 'IR16', 'VIS6', 'VIS8']
    The start and end dates must be in the format DD/MM/YYYY, in the range
    01/01/2019 to 01/01/2020 inclusive.
    """
    # Input validataion
    try:
        # first second of first day + final second of final day
        start_date = datetime(*np.flip(start.split('/')).astype(int), 0, 0, 0)
        end_date = datetime(*np.flip(end.split('/')).astype(int), 23, 59, 59)
    except ValueError:
        print("One or both dates entered are invalid")
    if start_date > end_date:
        raise ValueError("Start date after end date")
    if start_date < MIN_DATE:
        raise ValueError("Start date before 01/01/2019")
    if end_date > MAX_DATE:
        raise ValueError("Start date after 01/01/2020")
    if wavelength not in ['all', 'IR16', 'VIS6', 'VIS8']:
        raise ValueError("Invalid wavelength parameter.")

    # Get alphabetically + chronologically sorted list of files
    file_list = os.listdir(IMAGE_DIR)
    wavelength_list = []
    timestamp_list = []
    for file_name in file_list:
        file_wavelength = file_name[0:4]
        file_timestamp = datetime(int(file_name[29:33]),  # year
                                  int(file_name[33:35]),  # month
                                  int(file_name[35:37]),  # day
                                  int(file_name[37:39]),  # hour
                                  int(file_name[39:41]),  # minute
                                  int(file_name[41:43]))  # second
        wavelength_list.append(file_wavelength)
        timestamp_list.append(file_timestamp)
    sort_indices = np.lexsort((timestamp_list, wavelength_list))
    file_list = np.array(file_list)[sort_indices]
    timestamp_list = np.array(timestamp_list)[sort_indices]

    # Take slice of list for specific wavelengths
    # If wavelength == 'all', then no slice will be taken.
    third = int(file_list.size / 3)
    if wavelength == 'IR16':
        file_list = file_list[: third]
        timestamp_list = timestamp_list[: third]
    elif wavelength == 'VIS6':
        file_list = file_list[third: 2 * third]
        timestamp_list = timestamp_list[third: 2 * third]
    elif wavelength == 'VIS8':
        file_list = file_list[2 * third:]
        timestamp_list = timestamp_list[2 * third:]

    # Cut down file_list to only files within date range
    file_list = file_list[(timestamp_list >= start_date) &
                          (timestamp_list <= end_date)]

    # Load desired files into an array, and return it
    images = []
    for file_name in file_list:
        image = plt.imread(os.path.join(IMAGE_DIR, file_name))
        images.append(image)

    if wavelength == 'all':
        IR16, VIS6, VIS8 = np.array_split(images, 3)
        # Return in order of decreasing wavelength
        return IR16, VIS8, VIS6

    return np.asarray(images)
