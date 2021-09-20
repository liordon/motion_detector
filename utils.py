import os

def present(pipe_reader):
    opened_reader = os.fdopen(pipe_reader)
    for detection in opened_reader.readlines():
        if detection is None:
            break
        print(detection)

