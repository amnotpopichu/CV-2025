#exercise 2: greyscale
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
test_path = "visualchanger/test.png"

image1 = load(image1_path)
image2 = load(image2_path)
test = load(test_path)

def display(img):
    # Show image
    plt.figure(figsize = (5,5))
    plt.imshow(img)
    plt.axis('off')
    plt.show()
    
from skimage import color

def convert_to_grayscale(img):
    #hello this is my questionable code
    #i dont really know much about numpy so i decided to figure it out in the form of lists
    #according to google, i could have meaned it (which i tried but then couldn't figure out axes)
    #so instead, i used my highly questionable method of coding where i just did line by line and evaluated from there
    #im so sorry for the lack of comments, ill do my best to explain it but to be honest i sort of still dont get it (too many layers)
    '''img is an RGB image, represented as a 2D numpy array.'''
    # YOUR CODE GOES HERE
    np.save('my_array.npy', img)
    #print(img)
    #print("ajdslkjasfd")

    #easy way that i lowk dont understand: out = np.mean(img, axis=2)
    #big array that will be the 2d grey scale array
    arr2 = []

    #so it turns out theres row in img, then item in row, and then e in item. (num > list > 2d list (one line), >3d list, (the collection of the 2d lines))
    for row in img:
        #print("row")
        #print(row)

        #make a list for each pixel (greyscaled)
        arr1 = []
        for item in row:
            #print("item")
            #print(item)
            #make it greyscale with soem formula if ound on google
            arr1.append(item[0]*0.299+item[1]*0.587+0.114*item[2])
            #add it to the greyscale list
            my_array = np.array(arr1)

            #now in theory i have a 1d array with 4 items (when its a 4x4 image) (aka the first line)


            #print("printing")
            #print(my_array)
        #print("arr1")
        #print(my_array)
        
        #add the greyscale lists up
        #now there should be 4 lines of 4
        arr2.append(my_array)
        arr2thing = np.array(arr2)

    #print("jlakdsf")
    #print(arr2thing)


    out = arr2thing
    # END YOUR CODE
    return out

grey_image = convert_to_grayscale(image1)
display(image1)
#print("ima display")
display(grey_image)

#the print stuff is random things i aws figruing out for debugging
