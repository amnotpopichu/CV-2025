import cv2
import numpy as np
import mss
import time

def setup():
    #set up fps counter, pretty much justs define variables
    global new_frame_time, prev_frame_time
    new_frame_time = 0
    prev_frame_time = 0

def fps(frame):
    global new_frame_time, prev_frame_time
    #calculate fps by taking new time, then subtracting previous time, and doing 1/ all of that to get the fps
    #this works because it captures a frame each iteration, and if we use this time delta every single "frame" then we can calculate fps
    #tldr it works bc it counts time between frames, and from that you can get fps
    new_frame_time = time.time()
    fps = 1 / (new_frame_time - prev_frame_time)
    #reset frame time
    prev_frame_time = new_frame_time
    # Display FPS on the frame
    fps_text = f'fps: {str(int(fps))}'
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, fps_text, (10, 30), font, 1, (0, 0, 0), 2, cv2.LINE_AA)
    return frame

def img_process(frame):
    frame = cv2.GaussianBlur(frame, (7, 7), 3)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    threshold_value = 100
    frame[frame < threshold_value] = 0
    frame[frame > threshold_value] = 255
    return frame

def line_detection(frame):
    #Below is basic line detection with overlay, taken from stack overflow linked below
    #https://stackoverflow.com/questions/52816097/line-detection-with-opencv-python-and-hough-transform
    edges = cv2.Canny(frame, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=50, maxLineGap=10)
    if lines is not None:
        for line in lines:
            #print(line)
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    #print(lines)
    return frame, lines
def resize(frame):
    height, width = frame.shape[0], frame.shape[1]
    #crop (its in y,x not x,y)
    frame = frame[2*height//3 : height, width//3 : 2*width//3]
    return frame

#read frames
def main():
    #assume using main monitor
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        while True:
            #get sct.grab as a frame
            sct_img = sct.grab(monitor)
            frame = sct_img
            #convert to numpy array bc thats how opencv interprets images
            frame = np.array(frame)
            #resize
            frame = resize(frame)
            
            #if the frame doesnt exist, then exit
            if frame is None:
                print("Can't read frame")
                break
            
            frame = fps(frame)
            black_white = img_process(frame)
            lines_black_white, lines = line_detection(black_white)[0], line_detection(black_white)[1]
            print(lines)
            '''
            debugging stuff below
            not really debugging i guess its js a thing now
            well its just lines, aka lines just draw on screen, nothing else
            you really dont need to see what black and white looks like with the lines, you only need the lins
            from here i can develop this into getting individual lines and figuring out how to steer the car
            '''
            frame1 = frame.copy()
            frame1[frame1<=255] = 0
            lines1 = line_detection(frame)[1]
            if lines is not None:
                for line in lines1:
                    #print(line)
                    x1, y1, x2, y2 = line[0]
                    cv2.line(frame1, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            cv2.imshow("b w lines", frame1)
            cv2.imshow('color', frame)
            cv2.imshow('b&w', black_white)
            # Exit if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        #cleanup
        cv2.destroyAllWindows()


if __name__ == "__main__":
    setup()
    main()