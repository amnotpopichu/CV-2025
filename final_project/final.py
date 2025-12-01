import cv2
import numpy as np
import mss
import time

def setup():
    global new_frame_time, prev_frame_time
    new_frame_time = 0
    prev_frame_time = 0

def fps(frame):
    global new_frame_time, prev_frame_time
    new_frame_time = time.time()
    fps = 1 / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time
    fps_text = f'fps: {str(int(fps))}'
    # Display FPS on the frame
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
            sct_img = sct.grab(monitor)
            frame = sct_img
            frame = np.array(frame)
            if frame is None:
                print("Can't read frame")
                break
            
            frame = line_detection(frame)
            frame = fps(frame)
            cv2.imshow('lines in theory', frame)
            # Exit if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        #js clean up when loop is broken (when user presses q to exit out of frame reading)
        cv2.destroyAllWindows()
if __name__ == "__main__":
    setup()
    main()