# Processing EUMETSAT Images

This repository contains Ellis Hewins' and Mohammed Aslam's (a.k.a. Suhail's) code for the project "Remote sensing using EUMETSAT data", which forms part of the module "Imaging and Data Processing" of our masters year at Nottingham University.
The first four programs listed below were written by Suhail, and the next four programs by Ellis.

Note that the `images` folder is empty. On our local machines, this folder contains 2190 images from a geostationary meteorological satellite forming part of the EUMETSAT "meteosat" cluster. Given that the contents of this folder are 2.6 GB in size, it is not possible to store these images on GitHub. For access to these images, please contact Dr. Julian Onions.

## Dependencies

* numpy
* matplotlib
* scipy
* opencv
* scikit-image

## Files included

* `Load_clouds.py` - Includes two functions:
  - `clouds()`, which returns two arrays of the clouds and false image of earth with the clouds set to zero when given the week of data to analyse.
  - `Load_clouds()`, which return the same two array but uses the start and end dates for the range of images used. This is done by thresholding the images between a range of values and stacking images to produce coloured images.

* `Load_plots.py` - Uses the functions in `Load_clouds.py` to make plots that are used in the report. Image of earth, cloud detection image.

* `Submit_Ocean_detection.py` - Thresholding to extract the ocean and analyse in the infrared channel to analyse ocean current.

* `Cloud_detection.py` - Include a method to analyse cloud detection using gaussian smoothing, thresholding and dilation but this method is not used to produce result.

* `cloud_removal.py` - When run directly, this progarm loads the data files from the `images` directory into arrays with a week's worth of data. It then performs a weighted average of these images across time, where pixels with higher values are given lower weights. This allows clouds (which have high pixel values) to be removed from the images. Once a cloud-free image has been generaged, it is saved to the directory `cloud_free_images` to be used by other image and data processing algorithms. The program also contains a function, `single_pixel_tests()`, which when called produces one of the figures used in the report to demonstrate the different time-series smoothing methods that we experimented.

* `file_selection.py` - This program contains a range of functions used to load raw data from the `images` directory, and is imported by most of the other programs here. Different functions were used at different stages of development, but the most important function is `load_by_week()`. Nothing happens if `file_selection.py` is run directly.

* `general_statistics.py` - This program is used to generate a mean false-colour image from all the images in the data set, as well as one showing the standard deviation in each wavelength. The mean image is used by `NDVI.py` for display purposes in a figure defining the regions of interest. The standard deviation image is was not used in the report, but helped inform the decision of which aspects of the image would be interesting targets of further study (e.g. ocean currents).

* `NDVI.py` - This analyses the NDVI of the cloud free images in three regions, so can only be run after `cloud_removal.py` has been run first. It also performs analysis on cloud cover within these regions by importing `cloud()` from `Load_clouds.py`.
