# How to Run
1. Clone the repository with `git clone https://github.com/amnotpopichu/CV-2025`
2. Make sure you are in the project repo, and from there enter the subdirectory called final_project with `cd CV-2025/final_project/`
3. Install packages from requirements.txt: `pip install -r requirements.txt` (optionally with a virtual environment)
4. Open [slowroads.io](https://slowroads.io), and from there press begin, and wait for the car to load in.
5. Enter settings (on slowroads) with escape, and scroll until you find the "hide UI" button. Select that. While in settings, also go to controls and scroll until you find "toggle cinecam".
6. After exiting settings, press and hold on the car, and drag the mouse downwards to achieve a bird's eye view of the car.
7. Run final.py, and press o in the top left corner, bottom right, and the car corners (as shown in video) to calibrate
8. Drag the game's window below the windows that have been created by final.py
9. Zoom in and zoom out (as you would on a pdf) in the game, until lines are registered like the video below.
10. Press i to begin.




https://github.com/user-attachments/assets/482aa366-9ec4-41f9-9874-0db5203e32c3




# Results
I am pretty happy with the result, at first I thought I wasn't ambitious enough with my work, but as I worked through the project, I faced many issues and I finished with something that I can be proud of. While there are always ways to make it better, I think that it was good work, and a project that I can be happy with. More notes and limitations are noted below.
https://github.com/user-attachments/assets/1102b156-5b93-4042-ae10-10e0ea684133
# Process
## Project Overview


I really enjoy watching racing, especially Formula 1, along with racing and driving games. My original idea for this project was to create a basic "self driving car" in a game called Assetto Corsa on a server called NoHesi (which is a server that mods the cars and driving to drive on a highway with traffic bots, where the goal is to drive as fast as possible without crashing), but for this project, and so that I could work on this project at school, I have chosen an online io game called slowroads.io


The premise of the game is simple, it's a "zen driving game" where there is no racing, but nonetheless is a fun relaxing endless driving game, with most importantly, road lines and a centerline.


The idea is that I will be able to crop the image displayed on screen, and then from there, detect road lines and keep it driving, hopefully without crashing.


I was super inspired by the Waymos that drive around my home, and line following robots that I have seen on my social media feeds, pushing me to learn a little more about how the technology may work.


## Goals before starting
1. improve readability in code by using more functions, and better organization along with comments
2. create something I feel somewhat connected to, something that I can feel proud of but also something that pushes me while being something that I am interested in.
3. have fun and learn




## TLDR:
The way this project works is simple
- get screen capture (with mss)
- get a way to display data and overlay (with cv2)
- image process and detect roadlines (cv2 and HSV thresholds)
- drive and control the car using the data gathered




## Planning
- warp the image to only see what's in front, and crop the image to make it so that you can only see the roadlines and what's under to reduce the amount of junk on screen and speed up detection
- display lines for viewer through transparent window overlay
- find a way to control the car based on where lines are -- how to detect turns?


# Code Breakdown
## Setup
This function sets up the program, defines variables, and initiates calibration, and sets everything up. 

When calibrating, the program gets mouse position with pynput, and when the calibration key is pressed, it marks it for later calculations. 

## Screen capture
The goal for this first coding session is to start by just being able to capture the screen in a way that OpenCV can view it. Some of my options included mss, PIL, and forcing a screenshot using a hotkey, along with ffmpeg. While ffmpeg may be optimal, I will choose to use mss due to simplicity and performance.


### Result
For this, I chose to use mss, and to do fps testing, I used this helpful tutorial from [GeeksForGeeks](https://www.geeksforgeeks.org/python/python-displaying-real-time-fps-at-which-webcam-video-file-is-processed-using-opencv/). I found it to be pretty efficient at around 20 fps on average.
>![](images/fpstests.png "Doing a great job detecting everything except road lines, fps is dropping to a little less due to the complexity of the grass")
We can see the fps counter if you look closely at the top left, although it is very much covered by the fact that it is showing screen in screen, which is likely a significant contributor to the lower FPS in this image.


The code snippet is pretty simple, it uses mss, a cross platform python package to get a screenshot of the screen, and in practice is just an efficient method of grabbing the livestream frame by frame, in a way that OpenCV can handle.


~~~python
...
with mss.mss() as sct:
       print(top_left,bottom_right)
       monitor = {"top": top_left[1], "left": top_left[0], "width": bottom_right[0] - top_left[0], "height": bottom_right[1] - top_left[1]}
       print(monitor)
       while running:
           sct_img = sct.grab(monitor)
           frame = sct_img
           frame = np.array(frame)
           if frame is None:
               print("Can't read frame")
               break


~~~




## Overlay
One of the largest issues for this project is the fact that there is clearly a large OpenCV window displaying the debugging in the top left of our screen, so to solve this, it would be helpful to create a transparent window overlay above the desktop, that is click through and see through.


I'm really struggling with the overlay, the majority of my overlay code is in overlay_test.py, and is an adapted version of some code i found on [Stack Overflow](https://stackoverflow.com/questions/43666230/tkinter-create-canvas-that-overlays-screen-with-transparent-background), which was then adapted by Claude for MacOS use after I discovered that different platforms require different things. From there I attempted to understand what was going on, which can be seen in my comments.


I then tried to implement the overlay, in a separate file that won't be on the repository, but realized that it would be super complicated and very hard to actually read all the lines (and this is likely something that I could have solved if I had more time, and something that I may come back to one day).


>Just a quick disclosure note that while I set up the main structure combining the files, it seems that I don't understand the tk library well enough (due to all its funny loops), and because it's quite late as I work on this, I chose to have Claude combine the two while keeping the main functionality the same, just making them compatible without actually removing any key features. If i end up going with the final overlay, I will run through the code with full documentation if used


The current issue with the overlay that I am running into is that the code is currently built for a cv2 library, and the functions currently return the full frame, rather than just the lines. While I could try to maybe export each line separate, and return them as a list, that may be something else I try if I have time another day, but for now I think I will just crop the image in the next step, and then display the cv2 overlay somewhere else.


>![](images/overlaytest.png)


>TLDR: It only displays one line rather than all of them because my code isn't built for this


Update:
>![](images/overlay_2.png)
>![](images/overlay3.png)
I realized that rather than returning every item in the list, I could just return the whole list, allowing me to draw on screen. Another thing that I have realized is #1 how sensitive the line detection is, but also how the lines seem to be offset when compared to the first image, which is apparent in the fact that the lines that would be covering my sidebar seem to be offset downwards and to the right.




From here, I have two ways I could move forward, one using just regular OpenCV window in the top, and cropping the image (which I would do either way), and rather than having an invisible overlay, it would be a "live camera feed", or do significantly more work, and make debugging slightly harder and go for a full overlay.






Update again:
I tried to fix the offset, by finding the offset ~ (120x150), and then adjusting for that, but for some reason it seems to be locked into not fixing itself. I wonder if there's some hidden barriers that I can't access. For now I think I will proceed with keeping a live camera feed with cv2 rather than a full overlay.


Final code: This did not end up as an overlay, but rather three separate debugging windows with OpenCV. These windows allow me to debug, and show information.
>![](images/overlayagain.png)


## Image Cropping and Processing
<s>
We assume that our area of region will be in the bottom third of the screen, and the middle third. Our justification is that the screen will be set up the way that is outlined at the beginning in the section "setup". We also will be mainly concerned with what is directly in front of us, given the fact that the line detection struggles with lines that are far away and unclear.


~~~ python
def resize(frame):
   height, width = frame.shape[0], frame.shape[1]
   #crop (its in y,x not x,y)
   frame = frame[2*height//3 : height, width//3 : 2*width//3]
   return frame
~~~


From this, we can take the current frame, get its dimensions, which are the first two values of frame.shape()


Because OpenCV frames are merely just numpy arrays, we can use numpy splicing to cut off parts of the array. Height and width are in their respective positions due to the way that OpenCV handles it.


~~~ python
frame = frame[2*height//3 : height, width//3 : 2*width//3]
~~~


Let's break it down:
We are first concerned with the y side of things, so by splicing the array to only contain everything from the bottom 2/3 to the very bottom, we effectively only keep the bottom third. The same is with the x, where we take only the center third by cutting out the rest.


With respect to image processing, the code is simple. We start by converting the image to a grayscale image, from there convert it to black and white, given the argument threshold. From this, if it is below this threshold, it will turn the pixel white, and if greater, will turn it black. From this, we can now run line detection on it.
</s>

Because we already calibrate where the image would be, it allows us to cut most of this completely. From here we merely need to convert the image to black and white, which is done through HSV analysis, and cutting past a certain threshold. HSV is used because it gives us a very effective way of finding if it is too colorful (meaning we can disregard it), and if it is close to a bright (white) value. If not, we can remove it. This makes a great black and white image, where the white must be very white to work.
~~~ python
s_thresh = 35 # above is discarded (too colorful)
    v_thresh = 127 # above is white
    frame = (frame[:,:,1] < s_thresh) & (frame[:,:,2] > v_thresh)

    frame = frame.astype(np.uint8) * 255
    return frame
~~~

## Line Detection
For this, I used `cv2.HoughLinesP` to get the lines, where the code is mainly derived from [this](https://stackoverflow.com/questions/52816097/line-detection-with-opencv-python-and-hough-transform) Stack Overflow post, and adapted to fit my needs. The code is mainly simple, and just gets the lines, and returns the information. Along with this, it draws the lines on the screen.


~~~python
def line_detection(frame):
    edges = cv2.Canny(frame, 50, 150, apertureSize=3)
    sensitivity = 50
    lines = cv2.HoughLinesP(frame, 1, np.pi/180, sensitivity, minLineLength=100, maxLineGap=150)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)

    return frame, lines, edges
~~~

From there it is then interpreted in a separate function, with this following code:

~~~ python
if lines_bw is not None:
        for line in lines_bw:
            x1, y1, x2, y2 = line[0]
            if x2-x1 == 0:
                continue
            slope = (y2-y1)/(x2-x1)
            if abs(slope) <= 0.75: #remove horizontal lines
                pass
            else:
                slopes.append(slope)
                line_x_list.append((x1+x2)//2)
                cv2.line(only_lines, (x1, y1), (x2, y2), (255, 255, 255), 2)
        if slopes:
            for slope in slopes:
                slope_ave += slope

            linex = sum(line_x_list) // len(line_x_list)
            slope_ave = slope_ave/len(slopes)
        else:
            slope_ave = 0
~~~
This code does a few things:
1. removes horizontal lines, allowing me to discard lines that may be connected incorrectly, while removing any cause for misaligned driving
2. finds the average, allowing me to interpret all lines as one path forward
3. returns it all for the next driving function

## Driving
The driving function relies on the package `pynput`, and allows me to get and send inputs. The code simply checks if the program is "running", or if the user has set the code to run, which is triggered by the `i` key. If it does, then it will check if the car is too far from the "baseline", which is calculated by the car's position (grabbed from calibration in setup), along with using the x position of the car and average x position of the line. If it is too far, the car will steer towards the "centerline". With the slope calculated from the previous code block, it also lets me steer towards the line if it needs to make a turn. 

## TLDR
The workflow is as follows:
1. Gets frame
2. Converts to black and white
3. Runs line detection on the black and white image
4. Gets the slope of the lines from there, and with that information drives towards the centerline.

## Setbacks
This code went through a lot of iterations but here are some of the biggest ones.
1. Figuring out how to get input, this took a while to refactor some code to make it actually be able to run two while loops at once.
2. The driving function and slope took a while to think about and figure out how to work.
3. In the beginning, I couldn't get the lines to get detected, and had to try multiple things, before I fine-tuned the blur, along with the sensitivity.
## Limitations
I have a few known issues, and solutions to them (if I had a lot more time).
1. Overcorrection
2. Forever acceleration
3. Incorrect or lacking detection
4. Lack of threading


Addressing overcorrection, I learned that I could use a PID controller, which I didn't have the time to implement, or the knowledge. This would accumulate previous error, and would be able to correct it. This is also connected to a later issue, threading, where in theory, the code is waiting to finish correcting steering, before it can read the next frame, which could be fixed with threading (to my knowledge), but would require immense refactoring, and a lot of recoding, which I didn't have the time to, after I realized this issue. 

Another known issue is that it forever accelerates. I considered trying to find the friction coefficient, but instead due to other issues, it likely will fail before it reaches speeds that will make the program ineffective (or run into a wall slowing its speed first).

Sometimes, it also can't detect lines, which is almost impossible to fix due to the camera angles given. The only real solution here is the one I implemented, where if it can't find a line, it just drives based on the previous direction. Another possible idea, is a way that it would change the thresholding of the HSV along with the Hough Lines if no lines are present. 
## Reflection
Overall, I was pretty happy with this project, and it was a great way to end off a semester. While it can always be improved, I am proud to say that it was one of the best projects I have done so far, and has taught me so much about long term project management, and learning how to publish, with learning inline git, to writing my first readme, I am super proud of myself, and the amount of hours put in.
