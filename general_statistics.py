import os
import numpy as np
import matplotlib.pyplot as plt

import file_selection

file_list, _ = file_selection.sorted_filenames_and_dates()
IR16_files, VIS6_files, VIS8_files = np.array_split(file_list, 3)

image_shape = np.shape(plt.imread(os.path.join(file_selection.IMAGE_DIR,
                                               IR16_files[0])))
image_count = len(IR16_files)

# Calculating the yearly mean and standard deviation takes a while, so we save
# the result to a file and load that if the script has been run before.
if os.path.exists("whole_year_averaged_data.npy"):
    print("Average of image data already calculated, loading from file.")
    average_image = np.load("whole_year_averaged_data.npy")
else:
    average_image = np.zeros((*image_shape, 3))
    for n in range(image_count):
        average_image += np.stack((
            plt.imread(os.path.join(file_selection.IMAGE_DIR, IR16_files[n])),
            plt.imread(os.path.join(file_selection.IMAGE_DIR, VIS8_files[n])),
            plt.imread(os.path.join(file_selection.IMAGE_DIR, VIS6_files[n]))),
            axis=-1)
    average_image /= image_count
    print("Mean of image data calculated, saving to file.")
    np.save("whole_year_averaged_data.npy", average_image)

if os.path.exists("whole_year_standard_deviation_data.npy"):
    print("Std. deviation of image data already calculated, loading from file.")
    standard_deviation = np.load("whole_year_standard_deviation_data.npy")
else:
    standard_deviation = np.zeros((*image_shape, 3))
    for n in range(image_count):
        standard_deviation += (np.stack((
            plt.imread(os.path.join(file_selection.IMAGE_DIR, IR16_files[n])),
            plt.imread(os.path.join(file_selection.IMAGE_DIR, VIS8_files[n])),
            plt.imread(os.path.join(file_selection.IMAGE_DIR, VIS6_files[n]))),
            axis=-1) - average_image) ** 2
    standard_deviation = np.sqrt(standard_deviation / image_count)
    print("Standard deviation of image data calculated, saving to file.")
    np.save("whole_year_standard_deviation_data.npy", standard_deviation)

# Re-scale for display purposes
bright_std = 255 * standard_deviation / np.max(standard_deviation)

# Plot results
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6))
fig.tight_layout()
ax1.set_title("Mean over 1 year")
ax2.set_title("Standard deviation over 1 year")
ax1.set_axis_off()
ax2.set_axis_off()
ax1.imshow(average_image.astype(np.uint8))
ax2.imshow(bright_std.astype(np.uint8))

plt.show()
