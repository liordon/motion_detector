from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2
import os
import ast
import numpy as np
from utils import *


def detect_from_stream(input_pipe, output_pipe):
    counter = 0
    firstFrame = None

    opened_reader = os.fdopen(input_pipe)
    #while True:
    for frame_string in opened_reader.readlines():
    #    frame_string = opened_reader.readline()
        counter+=1
        if frame_string is None or frame_string == '':
            print("guess Im done after " + str(counter))
            break

        #gray_frame = np.array(ast.literal_eval(frame_string))
        gray_frame = string_to_frame(frame_string)
        #print(gray_frame)

        # if the first frame is None, initialize it
        if firstFrame is None:
            print("[DET-INFO] starting background model...")
            firstFrame = gray_frame.copy().astype("float")
            continue

        # accumulate the weighted average between the current frame and
        # previous frames, then compute the difference between the current
        # frame and running average
        cv2.accumulateWeighted(gray_frame, firstFrame, 0.05)

        frameDelta = cv2.absdiff(cv2.convertScaleAbs(gray_frame), cv2.convertScaleAbs(firstFrame))
        #frameDelta = cv2.absdiff(gray_frame, firstFrame)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        motion_rectangles = []
        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < 50:
                continue

            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            motion_rectangles += [((x,y),(x + w, y + h))]
        #print(motion_rectangles)
        frame_and_detections=frame_to_string(gray_frame) + "|" + str(motion_rectangles)+'\n'

        os.write(output_pipe, bytes(frame_and_detections,
            encoding='utf-8'))

    print("finished detecting")
    os.close(output_pipe)


