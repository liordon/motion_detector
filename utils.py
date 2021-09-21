import json
import os

import numpy as np


def present(pipe_reader):
    opened_reader = os.fdopen(pipe_reader)
    for detection in opened_reader.readlines():
        if detection is None:
            break
        print(detection)


def consume(pipe_reader):
    opened_reader = os.fdopen(pipe_reader)
    for detection in opened_reader.readlines():
        if detection is None:
            break


def _pixel_line_to_string(pixel_line):
    return '[' + ','.join([str(pixel) for pixel in pixel_line]) + ']'


def frame_to_string(pixel_array):
    return json.dumps(pixel_array.tolist())


def string_to_frame(serialized_frame):
    deserial = json.loads(serialized_frame)
    return np.asarray(deserial, dtype='float')

def log(component:str, message:str):
    print("[{}] - {}".format(component, message))