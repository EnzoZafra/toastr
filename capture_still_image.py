#######################################################################
#
# Script for taking a still image using built in webcam.
# 
# Notes:
# - Images are saved as ./images/{H:M_Y-m-d}__capture.png
#
# Usage: python3 capture_still_image.py
#
#######################################################################


import numpy as np
import cv2
import os
import sys
import datetime


TEXT_COLOR = (169, 147, 239)
FONT = cv2.FONT_HERSHEY_SIMPLEX
LINE_TYPE = cv2.LINE_AA
LINE_WIDTH = 1

# Get current date and time for image file name
IMAGE_FILENAME = "images/"+datetime.datetime.now().strftime("%H:%M_%Y-%m-%d")+"__capture.png"

global_frame = None
global_frame_with_text = None
cropping = False


def die():
    cv2.destroyAllWindows()
    source.release()
    sys.exit()


def swap(x, y):
    temp = x
    x = y
    y = temp
    return x, y


def mouse_crop(event, x, y, flags, param):
    global x_start, y_start, x_end, y_end, cropping
    global frame, global_frame, global_frame_with_text

    if event == cv2.EVENT_LBUTTONDOWN and cropping == False:
        x_start, y_start, x_end, y_end = x, y, x, y
        cropping = True

    elif event == cv2.EVENT_LBUTTONUP and cropping == True:
        x_end, y_end = x, y
        cropping = False

        if (x_start > x_end):
            x_start, x_end = swap(x_start, x_end)
        if (y_start > y_end):
            y_start, y_end = swap(y_start, y_end)

        refPoint = [(x_start, y_start), (x_end, y_end)]

        if len(refPoint) == 2:
            man_cropped = frame[refPoint[0][1]:refPoint[1][1], refPoint[0][0]:refPoint[1][0]]
            cv2.namedWindow("Manually Cropped Image")
            man_cropped_with_text = cv2.resize(man_cropped, (1028,720))
            cv2.putText(man_cropped_with_text, "Select this photo? (y/n)", (0, 50), FONT, 1.0, TEXT_COLOR, LINE_WIDTH, LINE_TYPE)
            global_frame_with_text = man_cropped_with_text
            global_frame = man_cropped


def angle_cos(p0, p1, p2):
    d1, d2 = p0-p1, p2-p1
    return np.dot(d1, d2) / (np.linalg.norm(d1) * np.linalg.norm(d2))


def find_squares(img):
    img = cv2.GaussianBlur(img, (5, 5), 0) 
    squares = []
    for gray in cv2.split(img):
        for thrs in range(0, 255, 26):
            if thrs == 0:
                bin = cv2.Canny(gray, 0, 50, apertureSize=5)
                bin = cv2.dilate(bin, None)
            else:
                retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
            # Get all contours in the image
            contours, hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            # Get 2 largest contour
            contours = sorted(contours, key = cv2.contourArea, reverse = True)[:2]
            for cnt in contours:
                cnt_len = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.02 * cnt_len, True)
                if len(approx) == 4 and cv2.contourArea(approx) > 500 and cv2.isContourConvex(approx):
                    approx = approx.reshape(-1, 2)
                    x, y, w, h = cv2.boundingRect(approx)
                    max_cos = np.max([angle_cos(approx[i], approx[(i + 1) % 4], approx[(i + 2) % 4]) for i in range(4)])
                    if max_cos < 0.5 and w < 1200 and h < 700:
                        squares.append(approx)
                        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 1)

    return squares, img


def crop_image(rects, img):
    cnt = 0

    for rect in rects:
        x_start, y_start, w, h = cv2.boundingRect(rect)
        refPoint = [(x_start, y_start), (x_start+w+2, y_start+h+2)]

        if len(refPoint) == 2:
            # Get the cropped image frame
            cropped_frame = img[refPoint[0][1]:refPoint[1][1], refPoint[0][0]:refPoint[1][0]]
            cropped_frame = cv2.resize(cropped_frame, (1028,720))
            cropped_window_name = "crop"+str(cnt)
            cv2.namedWindow(cropped_window_name)

            # Copy the cropped image and add text
            cropped_frame_with_text = cropped_frame.copy()
            cv2.putText(cropped_frame_with_text, "Select this photo? (y/n)", (0, 50), FONT, 1.0, TEXT_COLOR, LINE_WIDTH, LINE_TYPE)

            while(True):
                # Display the cropped image with text
                cv2.imshow(cropped_window_name, cropped_frame_with_text)
                # Get key input from user
                key = cv2.waitKey(1)
                # Save the photo by pressing 'y'
                if (key & 0xFF == ord("y")):
                    cv2.imwrite(IMAGE_FILENAME, cropped_frame)
                    cv2.destroyAllWindows()
                    return True
                    break
                # Close and don't save by pressing 'n'
                elif (key & 0xFF == ord("n")):
                    cv2.destroyWindow(cropped_window_name)
                    break
            cnt += 1       

    return False


if __name__ == "__main__":
    # Execute script from script dir
    if os.path.dirname(sys.argv[0]) != '':
        os.chdir(os.path.dirname(sys.argv[0]))

    # Create image directory if it doesn't exist
    if not os.path.exists("./images"):
        os.makedirs("./images")

    # Create video source object
    source = cv2.VideoCapture(0)

    # Capture a single frame from source
    ret, frame = source.read()

    print("Finding rectangles in image...")
    rects, new_frame = find_squares(frame)
    if (len(rects) == 0):
        print("No rectangles found in image")
        cv2.putText(new_frame, "No Rectangles Found", (0, 25), FONT, 1.0, TEXT_COLOR, LINE_WIDTH, LINE_TYPE)

    print("Cropping rectangles...")
    if (crop_image(rects, frame) is True):
        die()

    print("No cropped images selected, displaying original image...")
    cv2.putText(new_frame, "Use Mouse to Select Rect or", (0, 50), FONT, 1.0, TEXT_COLOR, LINE_WIDTH, LINE_TYPE)
    cv2.putText(new_frame, "Press 'q' to Exit", (0, 75), FONT, 1.0, TEXT_COLOR, LINE_WIDTH, LINE_TYPE)

    # Set up a mouse callback for manual cropping
    cv2.namedWindow("orig_image")
    cv2.setMouseCallback("orig_image", mouse_crop)

    while(True):
        if (global_frame is None):
            cv2.imshow("orig_image", new_frame)
            key = cv2.waitKey(1)
            if (key & 0xFF == ord("q")):
                die()
        else:
            cv2.imshow("Manually Cropped Image", global_frame_with_text)
            key = cv2.waitKey(1)
            if (key & 0xFF == ord("y")):
                cv2.imwrite(IMAGE_FILENAME, global_frame)
                die()
            elif (key & 0xFF == ord("n")):
                cv2.destroyWindow("Manually Cropped Image")
                global_frame = None
                continue

    die()
