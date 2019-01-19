#######################################################################
#
# Script for taking a still image using built in webcam.
# 
# Notes:
# - Press 'y' to save the captured image
# - Press 'q' to exit without saving image
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


# Execute script from script dir
os.chdir(os.path.dirname(sys.argv[0]))

# Create image directory if it doesn't exist
if not os.path.exists("./images"):
    os.makedirs("./images")

# Get current date and time for image file name
now = datetime.datetime.now()
image_file = "images/"+now.strftime("%H:%M_%Y-%m-%d")+"__capture.png"

# Create video source object
source = cv2.VideoCapture(0)

# Capture a single frame from source
ret, frame = source.read()

while(True):
    # Display the captured image
    cv2.imshow('img1',frame)
    # Get key input from user
    key = cv2.waitKey(0)
    # Save the photo by pressing 'y'
    if key & 0xFF == ord('y'):
        cv2.imwrite(image_file,frame)
        cv2.destroyAllWindows()
        break
    # Close and don't save by pressing 'q'
    elif key & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

source.release()