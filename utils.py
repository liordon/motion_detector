import os
import pickle
import json
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
    f = open("tmp", 'w')
    json.dump(pixel_array.tolist(), f)
    return json.dumps(pixel_array.tolist())
    #return str(pixel_array.dumps())
    #return str(pickle.dumps(pixel_array, protocol=0))
    #return '[' + ','.join([_pixel_line_to_string(pixel_line) for
    #    pixel_line in pixel_array]) + ']'
    
def string_to_frame(serialized_frame):
    deserial = json.loads(serialized_frame)
    #print(type(deserial))
    return np.asarray(deserial, dtype='float')
    #return np.loads(bytes(serialized_frame[:-1],
    #    encoding='utf-8'))
