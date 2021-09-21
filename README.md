# motion_detector
a small cv project that implements movement tracking and blurring

To activate, you can use `python orchestrator.py -v someVideo.mp4` and have the processes run on the video.

Alternatively, when activated without the -v argument, the video streamer pulls frames from the device's camera.

The orchestrator craetes 3 separate processes:
* The streamer (implemented in `streamer.py`) reads frames from the device's camera or a given mp4 file and streams downgraded frames via pipe.
* The detector (implemented in `detector.py`) recieves these frames and looks for movement in each frame by contrasting with the background. It forwards the frames along with the boundaries through another pipe.
* Finally the presenter (implemented in `presenter.py`) takes each frame and its detections, marks these detections' bounding boxes on top of the frame and blurs the inside.

Once the streamer finishes recieving input it closes the pipe and shuts down. Consequently, the detector does the same and finally the presenter.

helpful sources:
* [This motion detection guide](https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/)
* [Pythons multiprocess library](https://docs.python.org/3/library/multiprocessing.html)
