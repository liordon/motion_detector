from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2
import ast
import os
from utils import *

def present_annotated_frames_from_stream(pipe_reader):
    opened_reader = os.fdopen(pipe_reader)
    for message in opened_reader.readlines():
        if message is None:
            break
        frame_string, annotations = message.split('|')

        gray_frame = string_to_frame(frame_string)

        text = "unoccupied" if len(annotations) == 0 else "occupied"

        # loop over the contours
        for (bottom_left_corner, top_right_corner) in ast.literal_eval(annotations):
            cv2.rectangle(gray_frame, bottom_left_corner, top_right_corner, (0, 255, 0), 2)

        # draw the text and timestamp on the frame
        cv2.putText(gray_frame, "Room Status: {}".format(text), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(gray_frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, gray_frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        # show the frame and record if the user presses a key
        cv2.imshow("Security Feed", gray_frame)

    # cleanup the camera and close any open windows
    vs.stop() if args.get("video", None) is None else vs.release()
    cv2.destroyAllWindows()

