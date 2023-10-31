"""
This program loads which files for the data analysis process to use.
"""

import os
import re
import datetime
import numpy as np
import matplotlib.pyplot as plt

IMAGE_DIR = 'images'
MIN_DATE = datetime.datetime(2019, 1, 1)
MAX_DATE = datetime.datetime(2020, 1, 1)


def load_in_range(wavelength='all', start='01/01/2019', end='01/01/2020'):
    """
    This function is used to load files from a specific range of dates, in a
    specific wavelength.
    The variable 'wavelength' must be one of ['all', 'IR16', 'VIS6', 'VIS8']
    The start and end dates must be in the format DD/MM/YYYY, in the range
    01/01/2019 to 01/01/2020 inclusive.
    """
    # Input validataion
    try:
        start_date = datetime.datetime(*np.flip(start.split('/')).astype(int))
        end_date = datetime.datetime(*np.flip(end.split('/')).astype(int))
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

    # Work out valid dates within range
    date_strings = []
    current_date = start_date
    while current_date <= end_date:
        date_strings.append(current_date.strftime("%Y%m%d"))
        current_date += datetime.timedelta(days=1)

    # Get list of files for a given wavelength
    file_list = np.asarray(os.listdir(IMAGE_DIR))
    if wavelength == 'IR16':
        file_list = file_list[np.char.startswith(file_list, 'IR16')]
    if wavelength == 'VIS6':
        file_list = file_list[np.char.startswith(file_list, 'VIS6')]
    if wavelength == 'VIS8':
        file_list = file_list[np.char.startswith(file_list, 'VIS8')]

    # Get file names from file_list which contain a date from date_stings
    matching_files = [fname for fname in file_list if
                      any(re.search(dates, fname) for dates in date_strings)]

    # Load desired files into an array, and return it
    images = []
    for file_name in matching_files:
        image = plt.imread(IMAGE_DIR + '/' + file_name)
        images.append(image)

    return np.asarray(images)

