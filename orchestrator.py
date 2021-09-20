import os
import sys
from utils import present

camera_feed_reader, camera_feed_writer = os.pipe()
detection_reader, detection_writer = os.pipe()


if os.fork() > 0:  # top parent process becomes detector
    if os.fork() > 0: # second degree parent becomes streamer
        os.close(camera_feed_reader)
        os.close(detection_reader)
        os.close(detection_writer)
        for letter in "shambalulu":
            os.write(camera_feed_writer, bytes(letter + '\n',
            encoding="utf-8"))
        print("streamer finished writing")
        os.close(camera_feed_writer)
    else:

        # os.close(detection_reader)
        os.close(camera_feed_writer)
        print("detector starts reading")
        opened_reader = os.fdopen(camera_feed_reader)
        for letter in opened_reader.readlines():
            os.write(detection_writer, bytes(letter[:-1] +
                "ambalulu\n",
                encoding="utf-8"))
            print(letter)
        print("detector finished writing")
        os.close(camera_feed_reader)
        os.close(detection_writer)
        sys.stdout.flush()

else: # child becomes presenter
    print("presenter starts reading")
    os.close(camera_feed_reader)
    os.close(camera_feed_writer)
    os.close(detection_writer)
    present(detection_reader)
    print("presenter finished presenting")

print("done")
