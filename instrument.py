#!/usr/bin/env python
import operator
from threading import Lock

import cv2
from modules.util.opencv_webcam_multithread import WebcamVideoStream

vs = WebcamVideoStream().start()

def generate_outputs():
    # We return an array of six integers (0-255)
    # where each integer represents the arduino "analog" output
    return None

def send_to_arduino():
    # send a string of 6 characters( ascii val 0-255 to arduino)
    return None

def update_inputs_from_event(event):
    # An event should be a dictionary of inputs that should be updated
    global inputs
    INPUTS_LOCK.acquire()
    updated_input = {**inputs, **event}
    inputs = updated_input
    INPUTS_LOCK.release()
    # send_to_arduino(generate_outputs())
    print(inputs)

def update_face_rectangle(face):
    global face_rectangle
    face_rectangle = face['face']['faceRectangle']


from modules.input import emotion_input, arduino_input

emotion_input.getObservable().on('input',update_inputs_from_event)
arduino_input.getObservable().on('input',update_inputs_from_event)
# myo_input.getObservable().on('input',update_inputs_from_event)
emotion_input.getObservable().on('face',update_face_rectangle)

_OUTPUT_LOW = 0
_OUTPUT_HIGH = 255

output_ranges = ((0, 255), (0, 255), (0, 255), (0, 255), (0, 255), (0, 255)) #tuples
inputs = { 'soft_pot': 0, 'myo': {}, 'emotions': {} }
INPUTS_LOCK = Lock()

base_trim = 0
trims = ()
TRIMS_LOCK = Lock()

face_rectangle = {}

vs = WebcamVideoStream().start()



def renderResultOnImage(img):
    """Display the obtained results onto the input image"""
    faceRectangle = face_rectangle
    if 'left' in faceRectangle:
        cv2.rectangle(img, (faceRectangle['left'], faceRectangle['top']),
                      (faceRectangle['left'] + faceRectangle['width'], faceRectangle['top'] + faceRectangle['height']),
                      color=(255, 0, 0), thickness=5)

        if 'emotions' in inputs and 'anger' in inputs['emotions']:
            currEmotion = max(inputs['emotions'].items(), key=operator.itemgetter(1))[0]

            textToWrite = "%s" % (currEmotion)
            cv2.putText(img, textToWrite, (faceRectangle['left'], faceRectangle['top'] - 10), cv2.FONT_HERSHEY_SIMPLEX, 4,
                        (255, 0, 0), 10)


while True:
    ret, frame = vs.read()
    if ret:
        renderResultOnImage(frame)
        cv2.imshow('frame', cv2.resize(frame,(0,0),fx=.2,fy=.2))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break