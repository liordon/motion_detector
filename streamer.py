import cv2
import imutils
from imutils.video import VideoStream

from utils import *


def streamer_log(message: str):
    log("STRM", message)


def open_video_feed(video_path: str):
    # if the video argument is None, then we are reading from webcam
    if video_path is None:
        streamer_log("accessing camera")
        video_feed = VideoStream(src=0).start()
        time.sleep(2.0)

    # otherwise, we are reading from a video file
    else:
        streamer_log("using input file " + video_path)
        video_feed = cv2.VideoCapture(video_path)
    return video_feed


def forward_video_to_pipe(video_path: str, pipe):
    video_feed = open_video_feed(video_path)
    counter = 0
    # loop over the frames of the video
    while True:
        # grab the current frame and initialize the occupied/unoccupied
        frame = video_feed.read()
        frame = frame if video_path is None else frame[1]

        # if the frame could not be grabbed, then we have reached the end
        # of the video
        if frame is None:
            break

        # resize the frame, convert it to grayscale, and blur it
        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        pipe.send(frame_to_string(gray) + '\n')
        counter += 1

    video_feed.stop() if "stop" in dir(video_feed) is None else video_feed.release()
    streamer_log("streamer finished writing " + str(counter) + " frames")
    pipe.close()


if __name__ == "__main__":
    # construct the argument parser and parse the arguments
    import argparse
    import os

    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", help="path to the video file")
    ap.add_argument("-p", "--pipe", help="path to the pipe to stream frames into")
    ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
    args = vars(ap.parse_args())

    pipe_name = args.get("pipe")
    pipe_name = "camStream.pipe" if pipe_name is None else pipe_name
    if not os.path.exists(pipe_name):
        os.mkfifo(path=pipe_name)
    pipe_writer = open(pipe_name, 'w')

    streamer_log("video stream is open")
    forward_video_to_pipe(args.get("video", None), pipe_writer)
    os.close(pipe_writer)
    os.remove(pipe_name)
    streamer_log("video stream is closed")
