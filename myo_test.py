#!/usr/bin/env python
from myo import init, Hub, Feed
from decimal import *
import serial
import time

getcontext().prec = 4

init('sdk/myo.framework')
feed = Feed()
hub = Hub()
hub.run(1000, feed)


def arrayToStringWithMarker(array):
    return "<" + str(array) + ">"


try:
    myo = feed.wait_for_single_device(timeout=2.0)
    ard = serial.Serial('/dev/cu.usbmodem14311', timeout=2, baudrate=115200)
    time.sleep(2)
    if not myo:
        print("No Myo connected after 2 seconds")
    while hub.running and myo.connected:
        quat = myo.orientation
        strArray = [format(quat.x, '2.4f'), format(quat.y, '2.4f'), format(quat.z, '2.4f'), format(quat.w, '2.4f')]
        time.sleep(.01)
        print("arr: " + arrayToStringWithMarker(strArray))
        ard.write(arrayToStringWithMarker(strArray).encode())

        # print('Orientation:', format(quat.x,'2.4f'), format(quat.y,'2.4f'), format(quat.z,'2.4f'), format(quat.w,'2.4f'))

finally:
    hub.shutdown()  # !! crucial
