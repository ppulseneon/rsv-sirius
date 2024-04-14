import threading
import uuid

import cv2
import torch
import pathlib
pathlib.PosixPath = pathlib.WindowsPath

PROBABILITY = 0.85

def detect_parts(model, path):
    image = cv2.imread(path)
    results = model(image)

    returned = dict()


    detections = results.xyxy[0].tolist()
    '''
    for detection in detections:
        if detection[4] > PROBABILITY:
            cropped_image = image[int(detection[1]):int(detection[3]), int(detection[0]):int(detection[2])]
            filename = f'temp/{uuid.uuid4()}.jpg'
            cv2.imwrite(filename, cropped_image)

            returned[str(detection[5])] = filename
    '''

    def process_detection(detection, image):
        if detection[4] > PROBABILITY:
            cropped_image = image[int(detection[1]):int(detection[3]), int(detection[0]):int(detection[2])]
            filename = f'temp/{uuid.uuid4()}.jpg'
            cv2.imwrite(filename, cropped_image)

            returned[str(detection[5])] = filename

    threads = []
    for detection in detections:
        thread = threading.Thread(target=process_detection, args=(detection, image))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return returned
