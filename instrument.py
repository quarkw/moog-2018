#!/usr/bin/env python
import operator
from queue import Queue
from threading import Lock, Thread
import serial
from numpy import interp
import cv2
from modules.conductor import Conductor;
from modules.enums.interval import Interval;
from modules.enums.note import Note;
from modules.util.opencv_webcam_multithread import WebcamVideoStream

write_queue = Queue()

vs = WebcamVideoStream().start()
last_send_to_arduino = ''
last_note = 1000
conductor = Conductor()
conductor.set_bpm(200)
conductor.arpeggio_length = 3
conductor.interval = Interval.MAJOR3
conductor.arpeggio_speed = Note.ET
conductor.arpeggio_repeat = True


def generate_outputs():
    # We return an array of six integers (0-255)
    # where each integer represents the arduino "analog" output
    outputs = [0,0,0,0,0,0]
    if 'soft_pot' in inputs:
        if inputs['soft_pot'] > 100:
            outputs[0] = interp(inputs['soft_pot'],[1,1000],[30,110])
            if abs(outputs[0] - conductor.base_note) > 2:
                conductor.play(outputs[0])
    if 'myo' in inputs:
        (x,y,z) = inputs['myo']
        outputs[1] = interp(x,[-60,30],[0,255])
        outputs[2] = interp(y,[-90,90],[0,255])
        outputs[3] = interp(z,[-180,180],[0,255])
        conductor.set_bpm(interp(y,[-90,0,90],[5,100,1000]))

    if 'emotions' in inputs:
        currEmotion = max(inputs['emotions'].items(), key=operator.itemgetter(1))[0]
        if currEmotion == 'happiness':
            conductor.arpeggio_length = int(interp(z,[-90,90],[2,7]))
            # conductor.interval = Interval.MAJOR3
        else:
            conductor.arpeggio_length = int(interp(z,[-90,90],[1,4]))
            # conductor.interval = -Interval.Minor3

        # conductor.arpeggio_step = int(interp(z,[-150,150],[1,5]))

        if inputs['pose'] == 3:
            conductor.arpeggio_length = 0
            # conductor.
        # else:


    # print(list(outputs))
    outputs = map(lambda x: int(min(x, 255)), outputs)
    outputs = map(lambda x: 1 if x < 4 else x, outputs)
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
    # print("Sending: "+ str(list(map(lambda x: ord(x),string))) )

    try:
        # write_queue.put(string1.encode())
        # if arduino_input.getSerialPort().out_waiting() == 0:
        arduino_input.getSerialPort().write(string1.encode())
        arduino_input.getSerialPort().cancel_write()
        last_send_to_arduino = string
        global last_note
        last_note = ord(string[0])
    except:
        return None

def play_note(note):
    outputs = [0,0,0,0,0,0]
    outputs[0] = note
    outputs = map(lambda x: int(min(x, 255)), outputs)
    outputs = map(lambda x: 1 if x < 4 else x, outputs)
    send_to_arduino("".join(chr(i) for i in outputs))

conductor.obs.on('note',play_note)
conductor.play(60);

def update_inputs_from_event(event):
    # An event should be a dictionary of inputs that should be updated
    global inputs
    INPUTS_LOCK.acquire()
    updated_input = {**inputs, **event}
    inputs = updated_input
    INPUTS_LOCK.release()
    if 'soft_pot' in event:
        send_to_arduino(generate_outputs())
        # print(event)
    # if 'myo' in event:
    #     print(event)

def update_face_rectangle(face):
    global face_rectangle
    face_rectangle = face['face']['faceRectangle']


from modules.input import emotion_input, arduino_input, myo_input


def write_worker():
    while True:
        item = write_queue.get()
        arduino_input.getSerialPort().write(item)
        write_queue.task_done()

for i in range(10):
     t = Thread(target=write_worker)
     t.daemon = True
     t.start()


emotion_input.getObservable().on('input',update_inputs_from_event)
arduino_input.getObservable().on('input',update_inputs_from_event)
myo_input.getObservable().on('input',update_inputs_from_event)
emotion_input.getObservable().on('face',update_face_rectangle)

inputs = {}
INPUTS_LOCK = Lock()


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
    # None
    ret, frame = vs.read()
    if ret:
        renderResultOnImage(frame)
        cv2.imshow('frame', cv2.resize(frame,(0,0),fx=.2,fy=.2))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break