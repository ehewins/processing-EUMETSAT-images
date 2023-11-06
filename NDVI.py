import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

IMAGE_DIR = 'cloud_free_images'
# There are 52 images - one for each week of the year
cloud_free_files = ["week_{:d}.jpg".format(w) for w in range(52)]
image_shape = np.shape(plt.imread(os.path.join(IMAGE_DIR,
                                               cloud_free_files[0])))
image_count = len(cloud_free_files)

# Compute the Normalised Difference Vegetation Index for all images
# for file_name in cloud_free_files:
for file_name in cloud_free_files[:10]:
    image = plt.imread(os.path.join(IMAGE_DIR, file_name))
    NVDI = (image[:, :, 1] - image[:, :, 2]) / \
        (image[:, :, 1] + image[:, :, 2])
    vegetation = (NVDI >= 0.25) & (NVDI <= 0.8)
    display_image = np.copy(image)
    display_image[vegetation] = 255 * \
        np.stack((np.zeros_like(NVDI),
                  np.ones_like(NVDI),
                  np.zeros_like(NVDI)), axis=-1)[vegetation]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    ax1.imshow(image.astype(np.uint8))
    plt.imshow(display_image.astype(np.uint8))
    ax1.set_title("Original image")
    ax2.set_title("Highlighted vegetation")

plt.show()
