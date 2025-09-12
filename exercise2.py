#exercise 2

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
filter1 = np.array(
[
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,1],
    [0,0,0,0,0],
    [0,0,0,0,0]
])

filter2 = np.array(
[
    [0,0,0],
    [0,2,0],
    [0,0,0]
])

# Hint: check the lecture slides for a familiar-looking filter
filter3 = np.array(
[
    [-.11,-.11,-.11],
    [-.11,1.88,-.11],
    [-.11,-.11,-.11],
])

#had to check my sanity and make sure im actaully editing somehitng
#with open("output.txt", "w") as file:
#    file.write(str(image))

    
'''
channeledit = input("enter a channel to edit (0,1,2) for (r,g,b): pls do numbers im not really tryna do allat if then stuff rn ")
channelred = image.copy()
channelred = channelred[:,:,int(channeledit)]

channelred = naive_convolution_filter(channelred, filter2)


image[:,:,int(channeledit)] = channelred


'''
channelred = image.copy()
channelred = channelred[:,:,0]

channelred = naive_convolution_filter(channelred, filter3)


image[:,:,0] = channelred

channelgreen = image.copy()
channelgreen = channelgreen[:,:,1]

channelgreen = naive_convolution_filter(channelgreen, filter3)


image[:,:,1] = channelgreen


channelblue = image.copy()
channelblue = channelblue[:,:,1]

channelblue = naive_convolution_filter(channelblue, filter1)


image[:,:,2] = channelblue

#should shift the blue channel over 2 pixels, and nothing else (see exercise 1 work)

#with open("output1.txt", "w") as file:
#    file.write(str(image))

display(image)
display(channelred)
