# Processing EUMETSAT Images

This repository contains Ellis Hewins' and Mohammed Aslam's (a.k.a. Suhail's) code for the project "Remote sensing using EUMETSAT data", which forms part of the module "Imaging and Data Processing" of our masters year at Nottingham University.

Note that the `images` folder is empty. On our local machines, this folder contains 2190 images from a geostationary meteorological satellite forming part of the EUMETSAT "meteosat" cluster. Given that the contents of this folder are 2.6 GB in size, it is not possible to store these images on GitHub.


What each of the files do:

Load_clouds.py - Include two function: clouds(week) which returns two arrays of the clouds and false image of earth with the clouds set to zero when given the week of data to analyse. Load_clouds() which return the same two array but uses the start and end dates for the range of images used.
This is done by thresholding the images between a range of values and stacking images to produce coloured images.

Load_plots.py - Use the functions in Load_clouds to make plots that are used in the report. Image of earth, cloud detection image.

Submit_Ocean_detection.py - Thresholding to extract the ocean and analyse in the infrared channel to analyse ocean current.

Cloud_detection.py - include a method to analyse cloud detection using gaussian smoothing, thresholding and dilation but this method is not used to produce result.

cloud_removal - 

file_selection - Set up functions to obtain satellite images from given start and end date along with a function to extract a week worth of images.

general_statisstics.py - using standard deviation to find clouds which are far away from the mean value of the colour channel images to produce an image a cloud free image of the earth.

NDVI.py - Measuring vegetation and cloud coverage for Africa, South America, Europe and the middle east. Showing the correlation between the two.

cloud_removal - 





