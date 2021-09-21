from multiprocessing import Process, Pipe
from multiprocessing.spawn import freeze_support

import detector
import presenter
import streamer
import argparse

if __name__ == '__main__':
    freeze_support()
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", help="path to the video file")
    args = vars(ap.parse_args())

    camera_feed_reader, camera_feed_writer = Pipe(False)
    detection_reader, detection_writer = Pipe(False)

    streamer_process = Process(target=streamer.forward_video_to_pipe, args=(args.get("video", None), camera_feed_writer,))
    streamer_process.start()
    detector_process = Process(target=detector.detect_from_stream,
        args=(camera_feed_reader, detection_writer, streamer_process.pid))
    detector_process.start()
    presenter_process = Process(target=presenter.present_annotated_frames_from_stream,
        args=(detection_reader, detector_process.pid))
    presenter_process.start()

    streamer_process.join()
    detector_process.join()
    presenter_process.join()
