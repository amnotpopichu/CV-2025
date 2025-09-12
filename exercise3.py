#exercise 3

from skimage import io
import numpy as np
import matplotlib.pyplot as plt
from time import time

# Make matplotlib figures appear inline in the
# notebook rather than in a new window
plt.rcParams['figure.figsize'] = (10.0, 8.0) # set default size of plots
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

# provide methods for loading and displaying images
def load(image_path):
    out = io.imread(image_path)
    out = out.astype(np.float64) / 255
    return out

def display(img, title=None):
    # Show image
    plt.figure(figsize = (5,5))
    plt.imshow(img)
    plt.title(title)
    plt.axis('off')
    plt.show()

# As usual, you may use your own images, but you must include them in your submission.
#github doesnt let me upload images
image_path = 'filters/image3.jpeg'

image = load(image_path)

import math
def naive_convolution_filter(image, kernel):
    """
    Args:
        image: numpy array of shape (Hi, Wi).
        kernel: numpy array of shape (Hk, Wk).
    Returns:
        out: numpy array of shape (Hi, Wi).
    """
    out = np.zeros(image.shape)

    for image_row in range(image.shape[0]):
        for image_column in range(image.shape[1]):
            output_value = 0
            for kernel_row in range(kernel.shape[0]):
                for kernel_column in range(kernel.shape[1]):
                    image_row_offset = math.ceil(kernel_row - kernel.shape[0] / 2)
                    image_column_offset = math.ceil(kernel_column - kernel.shape[1] / 2)

                    if (image_row + image_row_offset < 0 or
                        image_row + image_row_offset >= image.shape[0] or
                        image_column + image_column_offset < 0 or
                        image_column + image_column_offset >= image.shape[1]):
                        image_value = 0
                    else:
                        image_value = image[image_row + image_row_offset, image_column + image_column_offset]

                    output_value += image_value * kernel[kernel_row, kernel_column]

            out[image_row, image_column] = output_value

    return out
#got this one from google 
sharpening2filter = np.array(
[
    [0, -1, 0],
    [-1, 5, -1],
    [0, -1, 0]
])
#tried to apply the same principle and got this
sharpeningfilter = np.array(
[
    [-1, -1, -1],
    [-1, 9, -1],
    [-1, -1, -1]
])

#this seems to work too (and it should in theory)
sharpeningfilter3 = np.array(
[
    [0, -1, 0],
    [0, 3, 0],
    [0, -1, 0]
])
#testing limiations on how little i can go
sharpeningfilter4 = np.array(
[
    [0, 0, 0],
    [0, 2, 0],
    [0, -1, 0]
])


#turns out this is also a really intersting way to filter sharpness
sharpagain = np.array(
[
    [0, 0, -1, 0, 0],
    [0, 0, 0, 0, 0],
    [-1, 0, 5, 0, -1],
    [0, 0, 0, 0, 0],
    [0, 0, -1, 0, 0]
])
#more sharpness i guess
sharp2 = np.array(
[
    [-1, 0, -1, 0, -1],
    [0, 0, 1, 0, 0],
    [-1, 1, 5, 1, -1],
    [0, 0, 1, 0, 0],
    [-1, 0, -1, 0, -1]
])


#it seems through some random sheer luck that i have made somewhat of an edge detection filter
#to be honest, im not sure why it works but it does
experiment = np.array(
[
    [-1, 0, -2, 0, -1],
    [0, 0, 1, 0, 0],
    [-2, 1, 1, 1, -2],
    [0, 0, 1, 0, 0],
    [-1, 0, -2, 0, -1]
])
#slihgtly better edge detection
experiment2 = np.array(
[
    [-1, 0, -2, 0, -1],
    [0, 0, 0, 0, 0],
    [-2, 0, 5, 0, -2],
    [0, 0, 0, 0, 0],
    [-1, 0, -2, 0, -1]
])
#12 works best, prob cuz the other numbers add up to 12
experiment3 = np.array(
[
    [-1, 0, -2, 0, -1],
    [0, 0, 0, 0, 0],
    [-2, 0, 12, 0, -2],
    [0, 0, 0, 0, 0],
    [-1, 0, -2, 0, -1]
])

#the more extreme the numbers the better it works it seems
experiment4 = np.array(
[
    [-3, 0, -2, 0, -3],
    [0, 0, 0, 0, 0],
    [-2, 0, 20, 0, -2],
    [0, 0, 0, 0, 0],
    [-3, 0, -2, 0, -3]
])
display(image, "Original Image")
display(naive_convolution_filter(image, experiment4), "Filtered Image")