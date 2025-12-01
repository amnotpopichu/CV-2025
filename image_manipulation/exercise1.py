#exercise 1: dimming
from skimage import io
import numpy as np
import matplotlib.pyplot as plt

# This code is to make matplotlib figures appear inline in the
# notebook rather than in a new window.
plt.rcParams['figure.figsize'] = (10.0, 8.0) # set default size of plots
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

def load(image_path):
    """Loads an image from a file path, returning a numpy array of shape(image_height, image_width, 3).
    """
    out = io.imread(image_path)

    # Convert the image to be in the range (0, 1)
    out = out.astype(np.float64) / 255
    return out
image1_path = 'visualchanger/image1.jpeg'
image2_path = 'visualchanger/image2.jpeg'

image1 = load(image1_path)
image2 = load(image2_path)

def display(img):
    # Show image
    plt.figure(figsize = (5,5))
    plt.imshow(img)
    plt.axis('off')
    plt.show()
    

def dim_image(img):
    '''img is an image, represented as a 2D numpy array.'''
    #only code written by me (mutiplies the RGB values by half to half the brightness)
    img = img * 0.5
    # YOUR CODE GOES HERE
    out = img
    # END YOUR CODE
    return out
    
dim_image2 = dim_image(image2)
display(image2)
display(dim_image2)