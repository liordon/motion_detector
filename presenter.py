import ast
import datetime

import cv2
import psutil

from utils import *


def presenter_log(message: str):
    log("PRST", message)


def present_annotated_frames_from_stream(pipe_reader, pid):
    presenter_log("presenter presents")
    while pipe_reader.poll(3) or psutil.pid_exists(pid):
        message = pipe_reader.recv()
        if message is None:
            if not psutil.pid_exists(pid):
                break
            else:
                continue
        frame_string = message.split('|')[0]
        annotations = message.split('|')[1]

        gray_frame = string_to_frame(frame_string)
        blurred_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

        text = "unoccupied" if len(annotations) == 0 else "occupied"

        # loop over the contours
        for (bottom_left_corner, top_right_corner) in ast.literal_eval(annotations):
            blur_mask = np.ones(gray_frame.shape, dtype=np.uint8)
            cv2.rectangle(blur_mask, bottom_left_corner, top_right_corner, 0, thickness=-1)
            gray_frame = np.where(np.logical_not(blur_mask), blurred_frame, gray_frame)
            cv2.rectangle(gray_frame, bottom_left_corner, top_right_corner, (0, 255, 0), 2)

        # draw the text and timestamp on the frame
        cv2.putText(img=gray_frame,
            text="Room Status: {}".format(text),
            org=(10, 20),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.5,
            color=(2, 2, 255),
            thickness=2)
        cv2.putText(img=gray_frame,
            text=datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
            org=(10, gray_frame.shape[0] - 10),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.35,
            color=(2, 2, 255),
            thickness=1)

        # show the frame and record if the user presses a key
        cv2.imshow("Security Feed", cv2.convertScaleAbs(gray_frame))
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key is pressed, break from the lop
        if key == ord("q"):
            break

    # cleanup the camera and close any open windows
    presenter_log("presenter finished presenting")
    cv2.destroyAllWindows()
