from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2
import os
import sys
from utils import *

def open_video_feed(video_path:str):
    # if the video argument is None, then we are reading from webcam
    if video_path is None:
        print("accessing camera")
        video_feed = VideoStream(src=0).start()
        time.sleep(2.0)

    # otherwise, we are reading from a video file
    else:
        print("using input file " + video_path)
        video_feed = cv2.VideoCapture(video_path)
    return video_feed



def forward_video_to_pipe(video_feed, pipe):
    counter = 0
    # loop over the frames of the video
    while True:
        # grab the current frame and initialize the occupied/unoccupied
        # text
        frame = video_feed.read()[1]
        ###~~~~~~print(frame)
        #frame = frame if args.get("video", None) is None else frame[1]

        # if the frame could not be grabbed, then we have reached the end
        # of the video
        if frame is None:
            break

        # resize the frame, convert it to grayscale, and blur it
        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        ###~~~~~print(gray)
        os.write(pipe, bytes(frame_to_string(gray)+'\n', encoding='utf-8'))
        #os.write(pipe, frame_to_string(gray))
        counter+=1
        if counter > 30:
            break
        
    video_feed.stop() if "stop" in dir(video_feed) is None else video_feed.release()
    print("streamer finished writing")
    os.close(pipe)


if __name__=="__main__":
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", help="path to the video file")
    ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
    args = vars(ap.parse_args())

    video_feed = open_video_feed(args.get("video", None))

    test_pipe_reader, test_pipe_writer = os.pipe()
    if os.fork() > 0:
        forward_video_to_pipe(video_feed, test_pipe_writer)
    else:
        os.close(test_pipe_writer)
        present(test_pipe_reader)

