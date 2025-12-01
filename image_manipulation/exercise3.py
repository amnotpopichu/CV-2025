#exercise 3: rgb exclusion
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

def rgb_exclusion(image, channel):
    """Return image **excluding** the rgb channel specified

    Args:
        image: numpy array of shape(image_height, image_width, 3).
        channel: str specifying the channel. Can be either "R", "G" or "B".

    Returns:
        out: numpy array of shape(image_height, image_width, 3).
    """
    #so it took me this 30. minutes to figrue out but it turns out that i need to MAEK A COPY .
    #i did not know this and apperntly it kept altering image and img which explains a lot 
    #anywyas now it works :D
    
    img = image.copy()
    for row in img:
        for item in row:
            if channel == "R":
                item[0] = 0 
            elif channel == "G":
                item[1] = 0
            elif channel == "B":
                item[2] = 0
            #rint(item)
    
    ### YOUR CODE GOES HERE
    out = img
    ### END YOUR CODE

    return out

without_red = rgb_exclusion(image1, 'R')
without_blue = rgb_exclusion(image1, 'B')
without_green = rgb_exclusion(image1, 'G')
display(image1)
print("Below is the image without the red channel.")
display(without_red)

print("Below is the image without the green channel.")
display(without_green)

print("Below is the image without the blue channel.")
display(without_blue)