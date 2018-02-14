## Georgia Tech Moog Hackathon
Georgia Tech hosted their 4th annual Moog Hackathon February 9 - 12, 2018. The goal of this is to create an instrument over 48 hours.


A Moog Synthesizer is For more information on what moog is, see [here](https://en.wikipedia.org/wiki/Moog_synthesizer).

## Motivation
The VCU CS department sent a team to Georgia Tech for their annual [Moog Competition](https://guthman.gatech.edu/moog-hackathon).
We had an interest in building an instrument and this was a great opportunity to make that happen.


## Tools/Frameworks Used
We used the following:
* [Myo Armband](https://www.myo.com/) - Its a bluetooth-connected accelerometer that can also read the EEG activity from your forearms to determine what “pose” your hand is in.
* [Arduino Uno (5V)](https://store.arduino.cc/usa/arduino-uno-rev3) - An easy to use micro-controller
* [Soft Potentiometer](https://www.sparkfun.com/products/8679) - It is a sensor for tracking position and is activated by a spring loaded wiper
* [Microsoft's emotion API](https://azure.microsoft.com/en-us/services/cognitive-services/emotion/) - An API that detects facial expressions

## The Instrument, High Level

The Uno receives data from the soft potentiometer and sends it to the program. Meanwhile, data is sent from the Myo and the
response from Microsoft's Emotion API to the input directory for processing and use in [instrument.py](instrument.py).
The soft potentiometer controls the base note which modifies the moog note by an octave.


## The Instrument, Low Level

Initially we used the Myo Armband to change the frequency and pitch based off of the physical location in 3-dimensional space
using the built in accelerometer. However, We are also able to access the using Myo gestures to perform different actions.
See [myo_input.py](modules/input/myo_input.py) for how we are getting the data and transforming it for use in [instrument.py](instrument.py).
The data received from the Myo was in the form of a quaternion. This [blog](http://developerblog.myo.com/quaternions/) does a good job at explaining
what quaternions are. We transformed the quaternions into Euler's angles to get the X, Y, and Z axis for ease of use in processing.


The soft potentiometer is used to change the base note by an octave. Depending on where the potentiometer has been touched,
the Uno will receive the touch point represented as an integer from 0-1023. That integer will be sent to [arduino-input.py](modules/input/arduino_input.py)
for use in instrument.py.


We are looking at the user's facial expression through the computer's webcam and is handled in [emotion_input.py](modules/input/emotion_input.py).
Depending on the facial expression expressed at the moment of capture (every 1 second), the bpm will change. For example, a face that displays
happiness will increase the beat per minute.

## See It In Action

Video to come.