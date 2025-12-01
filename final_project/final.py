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

def line_detection(frame):
    #Below is basic line detection with overlay, taken from stack overflow linked below
    #https://stackoverflow.com/questions/52816097/line-detection-with-opencv-python-and-hough-transform
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=50, maxLineGap=10)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
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
            
            #if the frame doesnt exist, then exit
            if frame is None:
                print("Can't read frame")
                break
            
            #process frame with line detection
            frame = line_detection(frame)
            #fps counter
            frame = fps(frame)
            #show frame
            cv2.imshow('lines in theory', frame)
            # Exit if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        #cleanup
        cv2.destroyAllWindows()


if __name__ == "__main__":
    setup()
    main()