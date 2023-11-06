"""
This program loads which files for the data analysis process to use.
"""

import os
from datetime import datetime, timedelta
# These two lines fix a problem with some images not loading properly
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

import numpy as np
import matplotlib.pyplot as plt

IMAGE_DIR = 'images'
MIN_DATE = datetime(2019, 1, 1, 0, 0, 0)
MAX_DATE = datetime(2020, 1, 1, 23, 59, 59)


def sorted_filenames_and_dates():
    """
    This function reads the names of the files in the IMAGE_DIR directory, and
    returns an alphabetically and chronologically ordered list of these file
    names, along with a list of datetime objects defining when each image was
    taken.
    """
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

    return file_list, timestamp_list


def load_dates(wavelength='all', start='01/01/2019', end='01/01/2020'):
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

    file_list, timestamp_list = sorted_filenames_and_dates()

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


def load_datetimes_three_colour(start, end):
    """
    This function is used to create an array of three-colour images spanning a
    time interval defined using datetime objects.
    Files start at 'start', and run up to but not including 'end'.
    """
    # Input validation
    if not isinstance(start, datetime):
        raise TypeError("Parameter 'start' must be a datetime object.")
    if not isinstance(end, datetime):
        raise ValueError("Parameter 'end' must be a datetime object.")
    if start > end:
        raise ValueError("Start date after end date")
    if start < MIN_DATE:
        raise ValueError("Start date before 01/01/2019")
    if end > MAX_DATE:
        raise ValueError("Start date after 01/01/2020")

    # Get all filenames and dates and store ones from the desired time interval
    file_list, timestamp_list = sorted_filenames_and_dates()
    file_list = file_list[(timestamp_list >= start) & (timestamp_list < end)]
    IR16_files, VIS6_files, VIS8_files = np.array_split(file_list, 3)

    colour_images = []
    for n in range(len(file_list) // 3):
        # Load three monochrome image files into one colour image
        image = np.stack((
            plt.imread(os.path.join(IMAGE_DIR, IR16_files[n])),
            plt.imread(os.path.join(IMAGE_DIR, VIS8_files[n])),
            plt.imread(os.path.join(IMAGE_DIR, VIS6_files[n]))), axis=-1)
        colour_images.append(image)

    return np.asarray(colour_images).astype(np.uint8)


def load_by_week(week, separate=False):
    """
    This function loads an array of images files based on week number, ranging
    from 0 to 51. The 'separate' parameter, if set to true, causes the images
    to be sent in separate arrays for each colour channel rather than the
    default of colour images.
    """
    if week < 0 or week > 51:
        raise ValueError("Param. 'week' must have a value between 0 and 51.")
    if not isinstance(week, int):
        raise TypeError("Param. 'week' must be an integer.")

    start = MIN_DATE + timedelta(weeks=week)
    end = MIN_DATE + timedelta(weeks=week + 1)

    # Get all filenames and dates and store ones from the desired time interval
    file_list, timestamp_list = sorted_filenames_and_dates()
    file_list = file_list[(timestamp_list >= start) & (timestamp_list < end)]
    IR16_files, VIS6_files, VIS8_files = np.array_split(file_list, 3)

    colour_images = []
    for n in range(len(file_list) // 3):
        # Load three monochrome image files into one colour image
        image = np.stack((
            plt.imread(os.path.join(IMAGE_DIR, IR16_files[n])),
            plt.imread(os.path.join(IMAGE_DIR, VIS8_files[n])),
            plt.imread(os.path.join(IMAGE_DIR, VIS6_files[n]))), axis=-1)
        colour_images.append(image)
    colour_images = np.asarray(colour_images)

    if separate is True:
        R = colour_images[:, :, :, 0].astype(np.uint8)
        G = colour_images[:, :, :, 1].astype(np.uint8)
        B = colour_images[:, :, :, 2].astype(np.uint8)
        return R, G, B

    return colour_images.astype(np.uint8)
