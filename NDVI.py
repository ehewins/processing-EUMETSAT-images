import os
import numpy as np
import matplotlib.pyplot as plt

from Load_clouds import clouds
from general_statistics import calculate_yearly_mean

IMAGE_DIR = 'cloud_free_images'
# There are 52 images - one for each week of the year
weeks = range(52)
cloud_free_files = ["week_{:d}.jpg".format(w) for w in weeks]

# Define y_min, y_max, x_min, x_max for regions of analysis
regions = {
    "Africa": [1350, 3000, 1250, 3350],
    "South America": [1400, 3200, 0, 700],
    "Europe & Middle East": [0, 900, 1500, 3250]
}

# # Display these regions for use in a figure
# mean_image = calculate_yearly_mean()
# plt.imshow(mean_image.astype(np.uint8))
# for r in regions:
#     # top left, top right, bottom left and bottom right corner coords
#     tl = [regions[r][2], regions[r][0]]
#     tr = [regions[r][3], regions[r][0]]
#     bl = [regions[r][2], regions[r][1]]
#     br = [regions[r][3], regions[r][1]]
#     plt.plot([tl[0], tr[0], br[0], bl[0], tl[0]],
#              [tl[1], tr[1], br[1], bl[1], tl[1]], linewidth=2)
# plt.show()

# Define dictionaries to store weekly values of the regions' properties
vegetation_area = {
    "Africa": [],
    "South America": [],
    "Europe & Middle East": []
}
mean_NDVI = {
    "Africa": [],
    "South America": [],
    "Europe & Middle East": []
}

# Compute the Normalised Difference Vegetation Index for all images
for file_name in cloud_free_files:
    image = plt.imread(os.path.join(IMAGE_DIR, file_name))
    NDVI = (image[:, :, 1] - image[:, :, 2]) / \
        (image[:, :, 1] + image[:, :, 2])
    vegetation = (NDVI >= 0.3) & (NDVI <= 0.8)
    for region_name, slice_def in regions.items():
        region_greenery = vegetation[slice_def[0]: slice_def[1],
                                     slice_def[2]: slice_def[3]]
        region_NDVI = NDVI[slice_def[0]: slice_def[1],
                           slice_def[2]: slice_def[3]]
        greenery_NDVI = region_greenery * region_NDVI
        green_area = np.sum(region_greenery)
        mean_greenery_NDVI = np.nanmean(greenery_NDVI[greenery_NDVI != 0])
        vegetation_area[region_name].append(green_area)
        mean_NDVI[region_name].append(mean_greenery_NDVI)
    # Uncomment the following lines to display regions satisfying the threshold
    # (Consider changing the 'weeks' variable to a smaller range for speed)
    # display_image = np.copy(image)
    # display_image[vegetation] = 255 * \
    #     np.stack((np.zeros_like(NDVI),
    #               np.ones_like(NDVI),
    #               np.zeros_like(NDVI)), axis=-1)[vegetation]
    # fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    # ax1.imshow(image.astype(np.uint8))
    # plt.imshow(display_image.astype(np.uint8))
    # ax1.set_title("Original image")
    # ax2.set_title("Highlighted vegetation")

# Perform similar analysis on clouds in the regions
cloud_coverage = {
    "Africa": [],
    "South America": [],
    "Europe & Middle East": []
}
# Involves performing the entire thresholding process, so this takes a while
for week in weeks:
    # Generate weekly cloud density maps
    weekly_clouds, _ = clouds(week)
    sum_cloud_coverage = np.sum(weekly_clouds, axis=0)
    for region, region_def in regions.items():
        region_coverage = sum_cloud_coverage[region_def[0]: region_def[1],
                                             region_def[2]: region_def[3]]
        cloud_coverage[region].append(np.sum(region_coverage))

# Rescale the area arrays so they show relative change from the mean value
for region in regions:
    vegetation_area[region] /= np.mean(vegetation_area[region])
    cloud_coverage[region] /= np.mean(cloud_coverage[region])

fig, ((ax1), (ax2), (ax3)) = plt.subplots(3, 1, figsize=(10, 14))
for region in regions:
    ax1.plot(mean_NDVI[region], label=region)
    ax2.plot(vegetation_area[region], label=region)
    ax3.plot(cloud_coverage[region], label=region)
for ax in (ax1, ax2, ax3):
    ax.legend(loc='upper right')
    ax.set_xlabel("Week number")
ax1.set_ylabel("Mean NDVI of vegetation")
ax2.set_ylabel("Relative area of vegetation")
ax3.set_ylabel("Relative cloud coverage")

plt.show()
