from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2
import os
import sys
from utils import present


def forward_video_to_pipe(video_feed, pipe):
    # loop over the frames of the video
    while True:
        # grab the current frame and initialize the occupied/unoccupied
        # text
        frame = vs.read()
        frame = frame if args.get("video", None) is None else frame[1]
        text = "Unoccupied"

        # if the frame could not be grabbed, then we have reached the end
        # of the video
        if frame is None:
            break

        # resize the frame, convert it to grayscale, and blur it
        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        print(gray)
        os.write(pipe, bytes(str(gray), encoding='utf-8'))
        
    print("finished transmitting")
    os.close(test_pipe_writer)


if __name__=="__main__":
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", help="path to the video file")
    ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
    args = vars(ap.parse_args())

    # if the video argument is None, then we are reading from webcam
    if args.get("video", None) is None:
        print("accessing camera")
        vs = VideoStream(src=0).start()
        time.sleep(2.0)

    # otherwise, we are reading from a video file
    else:
        print("using input file " + args["video"])
        vs = cv2.VideoCapture(args["video"])
    test_pipe_reader, test_pipe_writer = os.pipe()
    if os.fork() > 0:
        forward_video_to_pipe(vs, test_pipe_writer)
    else:
        os.close(test_pipe_writer)
        present(test_pipe_reader)
        print("finished recieving")

