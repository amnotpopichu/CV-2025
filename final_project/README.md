
# Project Overview

One of my biggest hobbies is racing, especially f1, along with racing and driving games. My orginal idea for this project was to create a basic "self driving car" in a game called Assetto Corsa on a server called NoHesi (which is a server that mods the cars and driving to drive on a highway with traffic bots, where the goal is to drive as fast as possible without crashing), but for this project, and so that I could work on this project at school, I have chosen an online io game called slowroads.io 

The premise of the game is simple, its a "zen driving game" where there is no racing, but nonetheless is a fun relaxing endless driving game, with most importantly, road lines and a centerline. 

The idea is that I will be able to crop the image displayed on screen, and then from there, detect road lines and keep it driving, hopefully without crashing.

# Goals before starting
1. improve readability in code by using more functions, and better organization along with comments
2. create something I feel somewhat connected to, something that I can feel proud of but also something that pushes me while being something that I am interested in.
3. have fun and learn

# Step 1: Planning
 - warp the image to only see whats infront, and crop the image to make it so that you can only see the roadlines and whats under to reduce the amount of junk on screen and speed up detection
 - display lines for viewer through transparent window overlay 
 - find a way to control the car based on where lines are -- how to detect turns?

# Step 2: Screen capture

The goal for this first coding session is to start by just being able to capture the screen in a way that OpenCV can view it. Some of my options included mss, PIL, and forcing a screenshot using a hotkey, along with ffmpeg. While ffmpeg may be optimal, I will chose to us mss due to simplicity and performance.

### Result
For this, I chose to use mss, and to do fps testing, I used this helpful tutorial from [GeeksForGeeks](https://www.geeksforgeeks.org/python/python-displaying-real-time-fps-at-which-webcam-video-file-is-processed-using-opencv/). I found it to be pretty efficient at around 20 fps on average.
>![FPS counter and basic overview](images/fpstests.png "Doing a great job detecting everything except road lines, fps is dropping to a little less due to the complexity of the grass")
We can see the fps counter if you look closely at the top left, although it is very much covered by the fact that it is showing screen in screen, which is likely a significant contributor to the lower FPS in this image.

The code snippet is pretty simple, it uses mss, a cross platform python package to get a screenshot of the screen, and in practice is just an efficent method of grabbing the livestream frame by frame, in a way that opencv can handle. 

~~~python
...

with mss.mss() as sct:
        monitor = sct.monitors[1]
        while True:
            sct_img = sct.grab(monitor)
            frame = sct_img
            frame = np.array(frame)
            ...
~~~

# Step __: Overlay 
One of the largest issues for this project is the fact that there is clearly a large opencv window displaying the debugging in the top left of our screen, so to solve this, it would be helpful to create a transparent window overlay above the desktop, that is clickthrough and see through. 
# Step __: Image Cropping
We assume that ___. Our justification is that __.
# Step __: Line Detection

# Reflection

