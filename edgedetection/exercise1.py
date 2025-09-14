from skimage import io
import numpy as np
import matplotlib.pyplot as plt
from time import time
import cv2
# Make matplotlib figures appear inline in the
# notebook rather than in a new window

plt.rcParams['figure.figsize'] = (10.0, 8.0) # set default size of plots
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParqams['image.cmap'] = 'gray'

def display(img, title=None):
    # Show image
    plt.figure(figsize = (5,5))
    plt.imshow(img)
    plt.title(title)
    plt.axis('off')
    plt.show()
filter = np.array(
[
    [1,0,-1]
])

image = cv2.imread('edgedetection/iguana.png')
result = cv2.filter2D(image, -1, filter)
display(result)