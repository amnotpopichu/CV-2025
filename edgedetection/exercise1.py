from skimage import io
import numpy as np
import matplotlib.pyplot as plt
from time import time
import cv2
# Make matplotlib figures appear inline in the
# notebook rather than in a new window

plt.rcParams['figure.figsize'] = (10.0, 8.0) # set default size of plots
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

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

image = cv2.imread('iguana.png')
result = cv2.filter2D(image, -1, filter)
display(result, title="orginal filtered image")

'''# Exercise 1
Let's try and address some of the problems that we found in lecture.

1. The image is dark, and it's hard to tell where the edges are that we found. How can we improve on this? Can we do this in a single filter?
2. The algorithm finds lots of edges, but we don't care about the dim pixels, since they're least likely to be edges. Could we filter out these pixels? Put another way, could we keep just the bright pixels?
3. We used a horizontal derivative filter. Create and run a vertical derivative filter. Should it look similar? Does it? Find an image where the horizontal and vertical derivative filters produce very different output.
4. How does the derivative filter respond to noise? Load and run the filter on the noisy_einstein image. Can you improve on this result?
'''

#1
filter2 = np.array(
[
    [0,0,0],
    [0,3,0],
    [0,0,0],
])
result = cv2.filter2D(result, -1, filter2)
display(result, title="Brightened Image")


#2
#print(result)
result[result < 100] = 0 #inline suggustion after attempting loops but further reading https://www.programiz.com/python-programming/numpy/boolean-indexing
display(result, title="Filtered Bright Pixels")

#3
filter3 = np.array(
[
    [0,1,0],
    [0,0,0],
    [0,-1,0]
])
vert = cv2.filter2D(image, -1, filter3)
vert = cv2.filter2D(vert, -1, filter2)

display(vert, title="Vertical Filtered Image")
horz = cv2.filter2D(image, -1, filter)
horz = cv2.filter2D(horz, -1, filter2)
display(horz, title="Horizontal Filtered Image brighted")
#The vertical filter picked up more "horizontal" edges, while the vertical picked up "horiziontal" edges (see markedup.png)

#4 it picks up a lot of the noise
noisy = cv2.imread('noisy_einstein.png')
'''
blur_filter = np.array([
    [1.0,2.0,1.0], 
    [2.0,4.0,2.0], 
    [1.0,2.0,1.0]])/16.0
noisy = cv2.filter2D(noisy, -1, blur_filter)
display(noisy, title="Noisy Image")
noisy = cv2.filter2D(noisy, -1, filter)
display(noisy, title="Noisy Image")
noisy = cv2.filter2D(noisy, -1, filter2)
display(noisy, title="Noisy Image")
noisy[noisy < 100] = 0

display(noisy, title="Noisy Image")
'''
display(noisy, title="Noisy Image")
noisy_edit = cv2.filter2D(noisy, -1, filter)
display(noisy_edit)
#horiziontal edge
#just a edge detected image, picking up a lot of the noise
blur = np.array([
    [1,1,1],
    [1,1,1],
    [1,1,1]])/9.0

#apply blur
noisy_edit = noisy.copy()
noisy_edit = cv2.GaussianBlur(noisy, (5, 5), 1.5)
display(noisy_edit)
#show noisy blurred
noisy_edit = cv2.filter2D(noisy_edit, -1, filter)
#apply edge 
noisy_edit = cv2.filter2D(noisy_edit, -1, filter2)
#brigten
noisy_edit[noisy_edit < 50] = 0
#remove dark pixels
display(noisy_edit)



#claude test -- claude made this up cuz i was wondering why iw asnt getting the results i wanted but its not working well tbh
#it said that combining the horizontal and vertical edges would help

#i fixed it
#my number for thresholding was too high but now claude and me get similar results !
#maybe vertical and horizitonal combined isnt super necessary
horz_edges = cv2.filter2D(noisy_edit, -1, filter)

# Vertical derivative (detects horizontal edges)
vert_edges = cv2.filter2D(noisy_edit, -1, filter3)


combined = np.sqrt(horz_edges.astype(float)**2 + vert_edges.astype(float)**2)
combined = np.clip(combined, 0, 255).astype(np.uint8)

display(combined, title="Combined Edges")

# Brighten and threshold
combined = cv2.filter2D(combined, -1, filter2)
combined[combined < 50] = 0
display(combined, title="Final Result")
