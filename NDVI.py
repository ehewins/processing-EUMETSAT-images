import os
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
from skimage.morphology import binary_closing

IMAGE_DIR = 'cloud_free_images'
# There are 52 images - one for each week of the year
cloud_free_files = ["week_{:d}.jpg".format(w) for w in range(5)]
image_shape = np.shape(plt.imread(os.path.join(IMAGE_DIR,
                                               cloud_free_files[0])))
image_count = len(cloud_free_files)

# Compute the Normalised Difference Vegetation Index for all images
detected_vegetation = np.empty((0, image_shape[0], image_shape[1]))
for file_name in cloud_free_files:
    image = plt.imread(os.path.join(IMAGE_DIR, file_name))
    NVDI = (image[:, :, 1] - image[:, :, 2]) / \
        (image[:, :, 1] + image[:, :, 2])
    vegetation = (NVDI >= 0.25) & (NVDI <= 0.8)
    detected_vegetation = np.append(detected_vegetation, [vegetation], axis=0)
    # display_image = np.copy(image)
    # display_image[vegetation] = 255 * \
    #     np.stack((np.zeros_like(NVDI),
    #               np.ones_like(NVDI),
    #               np.zeros_like(NVDI)), axis=-1)[vegetation]
    # fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    # ax1.imshow(image.astype(np.uint8))
    # plt.imshow(display_image.astype(np.uint8))
    # ax1.set_title("Original image")
    # ax2.set_title("Highlighted vegetation")

# Label each connected region to analyse how they change over time
for veg_map in detected_vegetation:
    binary_closing(veg_map, footprint=np.ones((15, 15)), out=veg_map)
    labelled_blobs = label(veg_map)
    props = regionprops(labelled_blobs)
    blob_areas = [x.area for x in props]
    # Find largest 10 areas, in descending order.
    largest_blobs_indices = np.argsort(blob_areas)[:-11:-1]
    largest_blobs_centroids = [props[i].centroid for i in largest_blobs_indices]
    plt.figure()
    plt.imshow(veg_map, cmap='gray')
    for n, centroid in enumerate(largest_blobs_centroids):
        plt.plot([centroid[1]], [centroid[0]], 'o', label='Number {:d}'.format(n))
    plt.legend()


plt.show()
