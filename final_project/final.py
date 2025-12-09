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


def blur(frame):
    frame = cv2.GaussianBlur(frame, (7, 7), 3)
    return frame

def black_white(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    threshold_value = 100
    frame[frame < threshold_value] = 0
    frame[frame > threshold_value] = 255
    return frame



def line_detection(frame):
    #Below is basic line detection with overlay, taken from stack overflow linked below
    #https://stackoverflow.com/questions/52816097/line-detection-with-opencv-python-and-hough-transform
    edges = cv2.Canny(frame, 50, 150, apertureSize=3)
    sensitivity = 10
    lines = cv2.HoughLinesP(frame, 1, np.pi/180, sensitivity, minLineLength=10, maxLineGap=200)

    
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return frame, lines, edges


def resize(frame):
    height, width = frame.shape[0], frame.shape[1]
    #crop (its in y,x not x,y)
    frame = frame[height//2 : 7*height//8, width//3 : 2*width//3]
    return frame

def connected(frame, blur, bw):
    threshold = cv2.threshold(bw, 0, 255,
    cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1] 
    analysis = cv2.connectedComponentsWithStats(threshold, 
                                            4, 
                                                cv2.CV_32S)
    (totalLabels, label_ids, values, centroid) = analysis

    # Initialize a new image to
    # store all the output components
    output = np.zeros(bw.shape, dtype="uint8")
    new_img = frame.copy()

    # Loop through each component
    for i in range(1, totalLabels):
    
        # Area of the component
        area = values[i, cv2.CC_STAT_AREA] 
        
        if (area > 140) and (area < 400):
            # Now extract the coordinate points
            x1 = values[i, cv2.CC_STAT_LEFT]
            y1 = values[i, cv2.CC_STAT_TOP]
            w = values[i, cv2.CC_STAT_WIDTH]
            h = values[i, cv2.CC_STAT_HEIGHT]
            
            # Coordinate of the bounding box
            pt1 = (x1, y1)
            pt2 = (x1+ w, y1+ h)
            (X, Y) = centroid[i]
            
            # Bounding boxes for each component
            cv2.rectangle(new_img,pt1,pt2,
                        (0, 255, 0), 3)
            cv2.circle(new_img, (int(X),
                                int(Y)), 
                    4, (0, 0, 255), -1)

            # Create a new array to show individual component
            component = np.zeros(frame.shape, dtype="uint8")
            componentMask = (label_ids == i).astype("uint8") * 255

            # Apply the mask using the bitwise operator
            component = cv2.bitwise_or(component,componentMask)
            output = cv2.bitwise_or(output, componentMask)
    return new_img

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
            

            blur_frame = blur(frame)
            black_white_frame = black_white(blur_frame)
            connection_bounding = connected(frame, blur_frame, black_white_frame)
            fps_frame = fps(frame)
            cv2.imshow("blur", blur_frame)
            cv2.imshow("bw", black_white_frame)
            cv2.imshow("please speed", connection_bounding)
            

            #lines_on_black_white, lines_bw, edges = line_detection(black_white_frame)[0], line_detection(black_white_frame)[1], line_detection(black_white_frame)[2]
            #cv2.imshow('edges', edges)
            
            '''
            debugging stuff below
            not really debugging i guess its js a thing now
            well its just lines, aka lines just draw on screen, nothing else
            you really dont need to see what black and white looks like with the lines, you only need the lins
            from here i can develop this into getting individual lines and figuring out how to steer the car
            '''

            '''
            #lines_bw is lines based on the black and white image  lines_black_white 
            only_lines = lines_on_black_white.copy()
            only_lines[only_lines<=255] = 0
            #set it all to black

            #lines_bw = line_detection(l)[1]
            if lines_bw is not None:
                for line in lines_bw:
                    print(line)
                    x1, y1, x2, y2 = line[0]
                    cv2.line(only_lines, (x1, y1), (x2, y2), (255, 255, 255), 2)
            
            
            cv2.imshow('blur', blur_frame)
            #cv2.imshow("only lines", only_lines)
            cv2.imshow('black and white', black_white_frame)
            cv2.imshow('lines on black and white', lines_on_black_white)
      `      '''
            
            # Exit if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        #cleanup
        cv2.destroyAllWindows()


if __name__ == "__main__":
    setup()
    main()