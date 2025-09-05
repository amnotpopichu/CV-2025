#exercise 1

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
image_path = '/Users/leohsia29/Documents/CV-2025/filters/image1.jpeg'

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
'''
My guess is that it may darken, because mutiplying everything by zero, 
and then keeping 1, (my theory is that it doesn matter where the 1 is, 
i could be wrong) will make evertyhing darker, becuase when mutiplying rgb by 0, 
it will be closer to black


Result: it shifted over. This does make sense, becuase the 1 is offeset from the center,
 it effectivly moves it over. My prediction was wrong because I thought it was taking the average, 
 of all the surrounding ones, when it wasnt.

'''

filter2 = np.array(
[
    [0,0,0],
    [0,2,0],
    [0,0,0]
])

# Hint: check the lecture slides for a familiar-looking filter

'''
I think that this will NOT offset this time, becuase it is in the center. 
I think that it will make the image brighter, becuase when mutipled by 2, it will 
bring the RGB closer to 255, which will in turn make it closer to white

Result:
it made it brighter

'''
filter3 = np.array(
[
    [-.11,-.11,-.11],
    [-.11,1.88,-.11],
    [-.11,-.11,-.11],
])

'''
Prediction: I think that this will only change the outside edges, 
because the -0.11*8 = -0.88 which cancels out the 1.88 in the middle.
So i thikn it may make the outside edges darker, while keeping the rest the same

'''


display(image, title="Original Image")
#display(naive_convolution_filter(image, filter1), title="Filter 1")
#display(naive_convolution_filter(image, filter2), title="Filter 2")
display(naive_convolution_filter(image, filter3), title="Filter 3")

display(filter1, title="Filter 1")
display(filter2, title="Filter 2")
display(filter3, title="Filter 3")