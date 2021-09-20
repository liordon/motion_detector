import ast
import datetime

import cv2
import psutil

from utils import *


def present_annotated_frames_from_stream(pipe_reader, pid):
    print("presenter presents")
    while psutil.pid_exists(pid):
        message = pipe_reader.recv()
        if message is None:
            if not psutil.pid_exists(pid):
                break
            else:
                continue
        frame_string = message.split('|')[0]
        annotations = message.split('|')[1]

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
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key is pressed, break from the lop
        if key == ord("q"):
            break

    # cleanup the camera and close any open windows
    print("presenter finished presenting")
    cv2.destroyAllWindows()
