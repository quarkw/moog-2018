#!/usr/bin/env python
import operator
from threading import Lock
import serial
import cv2
from modules.util.opencv_webcam_multithread import WebcamVideoStream

vs = WebcamVideoStream().start()
last_send_to_arduino = ''

def generate_outputs():
    # We return an array of six integers (0-255)
    # where each integer represents the arduino "analog" output
    outputs = [0,0,0,0,0,0]
    if 'soft_pot' in inputs:
        if inputs['soft_pot'] > 100:
            outputs[0] = inputs['soft_pot']/4
    if 'myo' in inputs:
        (x,y,z) = list(map(lambda x: (x+180)/2,inputs['myo']))
        outputs[1] = x
        outputs[2] = y
        outputs[3] = z

    if 'emotions' in inputs:
        currEmotion = max(inputs['emotions'].items(), key=operator.itemgetter(1))[0]

    outputs = map(lambda x: int(min(x, 255)), outputs)
    outputs = map(lambda x: 1 if x < 4 else x, outputs)
    # print(list(outputs))
    return "".join(chr(i) for i in outputs)

def send_to_arduino(string):
    global last_send_to_arduino
    # send a string of 6 characters( ascii val 0-255 to arduino)
    # print(string.encode())
    # string = 'abcdef']
    if string == last_send_to_arduino:
        return None
    string1 = chr(2)+ string + chr(3)
    # print(len(string))
    # print("Sending: " + string)
    arduino_input.getSerialPort().write(string1.encode())
    last_send_to_arduino = string
    return None

def update_inputs_from_event(event):
    # An event should be a dictionary of inputs that should be updated
    global inputs
    INPUTS_LOCK.acquire()
    updated_input = {**inputs, **event}
    inputs = updated_input
    INPUTS_LOCK.release()
    if 'soft_pot' in event:
        send_to_arduino(generate_outputs())
    #     print(event)

def update_face_rectangle(face):
    global face_rectangle
    face_rectangle = face['face']['faceRectangle']


from modules.input import emotion_input, arduino_input, myo_input

inputs = {}
INPUTS_LOCK = Lock()

emotion_input.getObservable().on('input',update_inputs_from_event)
arduino_input.getObservable().on('input',update_inputs_from_event)
myo_input.getObservable().on('input',update_inputs_from_event)
emotion_input.getObservable().on('face',update_face_rectangle)

_OUTPUT_LOW = 0
_OUTPUT_HIGH = 255

output_ranges = ((0, 255), (0, 255), (0, 255), (0, 255), (0, 255), (0, 255)) #tuples

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