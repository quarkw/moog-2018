#!/usr/bin/env python
import operator
import time
import os
from functools import reduce

import requests
import cv2

_key = os.environ['MS_EMOTION_KEY']
_url = "https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize"
_maxNumRetries = 10
_faceDetectionScaleDown = .25;
_faceeDeteectionScaleUp = 4;

cap = cv2.VideoCapture(0)

timestamp = int(time.time())
lastResult = None;

headers = dict()
headers['Ocp-Apim-Subscription-Key'] = _key
headers['Content-Type'] = 'application/octet-stream'

json = None
params = None

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def processRequest(json, data, headers, params):
    """
    Helper function to process the request to Project Oxford

    Parameters:
    json: Used when processing images from its URL. See API Documentation
    data: Used when processing image read from disk. See API Documentation
    headers: Used to pass the key information and the data type request
    """

    retries = 0
    result = None

    while True:

        response = requests.request('post', _url, json=json, data=data, headers=headers, params=params)

        if response.status_code == 429:

            print("Message: %s" % (response.json()['error']['message']))

            if retries <= _maxNumRetries:
                time.sleep(1)
                retries += 1
                continue
            else:
                print('Error: failed after retrying!')
                break

        elif response.status_code == 200 or response.status_code == 201:

            if 'content-length' in response.headers and int(response.headers['content-length']) == 0:
                result = None
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str):
                if 'application/json' in response.headers['content-type'].lower():
                    result = response.json() if response.content else None
                elif 'image' in response.headers['content-type'].lower():
                    result = response.content
        else:
            print("Error code: %d" % (response.status_code))
            print("Message: %s" % (response.json()['error']['message']))

        break

    return result

def getFaceArea(face):
    return face['faceRectangle']['width'] * face['faceRectangle']['height']

def renderResultOnImage(result, img):
    global lastResult
    """Display the obtained results onto the input image"""
    # Find the largest face in the result set
    def convertCv2FaceToMsFace(cv2Face):
        if'faceRectangle' in cv2Face:
            return cv2Face
        cv2Face = list(map(lambda x: x * _faceeDeteectionScaleUp,cv2Face))
        return { 'faceRectangle': {'left': cv2Face[0], 'top': cv2Face[1], 'width': cv2Face[2], 'height': cv2Face[3]} }
    result = list(map(convertCv2FaceToMsFace, result))

    def returnBiggerFace(faceA, faceB) :
        faceAArea = getFaceArea(faceA)
        faceBArea = getFaceArea(faceB)
        if faceAArea > faceBArea:
            return faceA
        elif faceBArea > faceAArea:
            return faceB
        elif faceB['faceRectangle']['left'] < faceA['faceRectangle']['left']:
            return faceB
        elif faceA['faceRectangle']['left'] < faceB['faceRectangle']['left']:
            return faceA
        elif faceB['faceRectangle']['top'] < faceA['faceRectangle']['top']:
            return faceB
        else:
            return faceA
    print (result)
    if not result:
        return
    currFace = reduce(returnBiggerFace, result, result[0])

    if 'scores' in currFace:
        lastResult = currFace

    faceRectangle = currFace['faceRectangle']
    cv2.rectangle(img, (faceRectangle['left'], faceRectangle['top']),
                  (faceRectangle['left'] + faceRectangle['width'], faceRectangle['top'] + faceRectangle['height']),
                  color=(255, 0, 0), thickness=5)

    if lastResult and 'scores' in lastResult:
        currEmotion = max(lastResult['scores'].items(), key=operator.itemgetter(1))[0]

        textToWrite = "%s" % (currEmotion)
        cv2.putText(img, textToWrite, (faceRectangle['left'], faceRectangle['top'] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (255, 0, 0), 1)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    jpg = cv2.imencode('.jpg', frame)[1].tostring()

    gray = cv2.resize(gray,(0,0),fx=_faceDetectionScaleDown,fy=_faceDetectionScaleDown)

    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    # print(faces)
    if int(time.time()) - timestamp > 3:
        result = processRequest(json, jpg, headers, params)
        if result is not None:
            timestamp = int(time.time())
            # Load the original image from disk
            renderResultOnImage(result, frame)
    else:
        renderResultOnImage(faces,frame)
    cv2.imshow('frame',frame)

# Display the resulting frame
# cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

