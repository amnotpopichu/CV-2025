import cv2
import numpy as np
import mss
import time
from pynput.keyboard import Key, Listener, KeyCode
from pynput.keyboard import Key, Listener, KeyCode, Controller as KeyboardController
from pynput.mouse import Controller as MouseController

def setup():
    global driving
    driving = False
    print("When asked to calibrate, move your mouse to the desired position (top left or bottom right) and press 'o' to record it. Do not press any keys before prompted, and do not include the car in the calibration area. Press 'q' to quit anytime.")
    #set up fps counter, pretty much justs define variables
    global new_frame_time, prev_frame_time, pressed_keys, running, listener
    new_frame_time = 0
    prev_frame_time = 0
    pressed_keys = set()
    running = True
    listener = Listener(on_press=on_press, on_release=on_release)
    listener.start()
    #0 for top left, 1 for bottom right
    top_left = calibrate(0)
    bottom_right = calibrate(1)
    car_top_left = calibrate(2)
    car_bottom_right = calibrate(3)
    return top_left, bottom_right, car_top_left, car_bottom_right


def on_press(key):
    global pressed_keys
    pressed_keys.add(key)

def on_release(key):
    global running
    pressed_keys.discard(key)
    
def calibrate(num):
    global pressed_keys
    if num == 0:
        print("Awaiting top left corner... Press 'o' to record position:")
    elif num == 1:
        print("Awaiting bottom right corner... Press 'o' to record position:")
    if num == 2:
        print("Awaiting car top left corner... Press 'o' to record position:")
    elif num == 3:
        print("Awaiting car bottom right corner... Press 'o' to record position:")
    while True:
        if KeyCode.from_char('o') in pressed_keys:
            mouse = MouseController()
            pos = mouse.position
            time.sleep(0.5)
            #print(mouse.position)
            return pos
            
        
        


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
    threshold_value = 140
    frame[frame < threshold_value] = 0
    frame[frame > threshold_value] = 255
    return frame



def line_detection(frame):
    #Below is basic line detection with overlay, taken from stack overflow linked below
    #https://stackoverflow.com/questions/52816097/line-detection-with-opencv-python-and-hough-transform
    edges = cv2.Canny(frame, 50, 150, apertureSize=3)
    sensitivity = 50
    lines = cv2.HoughLinesP(frame, 1, np.pi/180, sensitivity, minLineLength=100, maxLineGap=150)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)

    return frame, lines, edges

def frame_only_lines(frame, black_white_frame):
    only_lines = frame.copy()
    only_lines[only_lines<=255] = 0
    lines_bw = line_detection(black_white_frame)[1]
    slopes = []
    slope_ave=0
    line_x_list = []
    linex = -1
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
    return only_lines, slope_ave, linex

def drive(slope_ave, linex, car_center_x, car_center_y):
    global driving
    delay = 0.15
    if KeyCode.from_char('i') in pressed_keys:
        driving = not driving
        time.sleep(0.5)
    keyboard = KeyboardController()
    
    
    if driving:
        x_offset = linex - car_center_x
        threshold = 30
        if linex == -1:
            keyboard.press('w')
            time.sleep(delay/1.7)
            keyboard.release('w')
            return 0, -1
        keyboard.press('w')
        time.sleep(delay/1.3)
        keyboard.release('w')
        #if x offset > 0, then turn right
        
        if x_offset > threshold:
            keyboard.press('d')
            time.sleep(delay)
            keyboard.release('d')
            return 1, 0
        elif x_offset < -threshold:
            keyboard.press('a')
            time.sleep(delay)
            keyboard.release('a')
            return -1, 0
        else:    
            if slope_ave == 0:
                return 0, -1
            elif slope_ave < 0:
                keyboard.press('d')
                time.sleep(delay)
                keyboard.release('d')
                return 1, 1
            elif slope_ave > 0:
                keyboard.press('a')
                time.sleep(delay)
                keyboard.release('a')
                return -1, 1
    else:
        return 0, -1

#read frames
def main(top_left, bottom_right, car_top_left, car_bottom_right):
    global driving
    prev_slope_ave = 0
    #assume using main monitor
    with mss.mss() as sct:
        print(top_left,bottom_right)
        monitor = {"top": top_left[1], "left": top_left[0], "width": bottom_right[0] - top_left[0], "height": bottom_right[1] - top_left[1]}
        print(monitor)
        while running:
            #get sct.grab as a frame
            sct_img = sct.grab(monitor)
            frame = sct_img
            #convert to numpy array bc thats how opencv interprets images
            frame = np.array(frame)
            #resize
            #frame = resize(frame)
            
            #if the frame doesnt exist, then exit
            if frame is None:
                print("Can't read frame")
                break
            car_y1 = int(car_top_left[1] - top_left[1])
            car_y2 = int(car_bottom_right[1] - top_left[1])
            car_x1 = int(car_top_left[0] - top_left[0])
            car_x2 = int(car_bottom_right[0] - top_left[0])
            car_center_x = (car_x1 + car_x2) // 2
            car_center_y = (car_y1 + car_y2) // 2

            frame[car_y1:car_y2, car_x1:car_x2] = 0
            
    
            blur_frame = blur(frame)
            black_white_frame = black_white(blur_frame)
            only_lines, slope_ave, linex = frame_only_lines(frame, black_white_frame)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(only_lines, str(round(slope_ave, 2)), (10, 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
            x_offset = linex - car_center_x
            cv2.putText(only_lines, str(round(x_offset, 3)), (10, 70), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(only_lines, str(driving), (130, 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
            if slope_ave != 0:
                drive_slope = slope_ave
                prev_slope_ave = slope_ave
            else:
                drive_slope = prev_slope_ave
            direction, cause = drive(drive_slope, linex, car_center_x, car_center_y)
            
            if linex == -1:
                cv2.putText(only_lines, "no lines", (100, 70), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
            elif direction == 1 and cause == 0:
                cv2.putText(only_lines, "turning right cause: baseline", (100, 70), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
            elif direction == -1 and cause == 0:
                cv2.putText(only_lines, "turning left cause: baseline", (100, 70), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
            elif direction == 1 and cause == 1:
                cv2.putText(only_lines, "turning right cause: direction", (100, 70), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
            elif direction == -1 and cause == 1:
                cv2.putText(only_lines, "turning left cause: direction", (100, 70), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
            else:
                cv2.putText(only_lines, "yay it worked", (100, 70), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
            
            fps_frame = fps(frame)
            cv2.imshow("blur", blur_frame)
            cv2.imshow("lines", line_detection(black_white_frame)[0])
            cv2.imshow("only lines", only_lines)
            #cleanup
            # Exit if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        #cleanup
        cv2.destroyAllWindows()
        listener.stop()


if __name__ == "__main__":
    top_left, bottom_right, car_top_left, car_bottom_right = setup()
    main(top_left, bottom_right, car_top_left, car_bottom_right)





#Below are either testing functions, or ones that were used and then removed later
'''

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
'''

