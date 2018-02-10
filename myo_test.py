#!/usr/bin/env python
from myo import init, Hub, Feed
from decimal import *
import serial
import time
import math

getcontext().prec = 4

init('sdk/myo.framework')
feed = Feed()
hub = Hub()
hub.run(1000, feed)

def arrayToStringWithMarker(array):
    return "<" + str(array) + ">"


def quaternionToEuler(w, x, y, z):
    ysqr = y * y

    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + ysqr)
    X = math.degrees(math.atan2(t0, t1))

    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    Y = math.degrees(math.asin(t2))

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (ysqr + z * z)
    Z = math.degrees(math.atan2(t3, t4))

    return [format(X, '2.3f'), format(Y, '2.3f'), format(Z, '2.3f')]


try:
    myo = feed.wait_for_single_device(timeout=2.0)                              #connecting to Myo
    ard = serial.Serial('/dev/cu.usbmodem14311', timeout=2, baudrate=115200)    #connecting to arduino
    time.sleep(2)                                                               #Sync with arduino
    if not myo:
        print("No Myo connected after 2 seconds")
    while hub.running and myo.connected:
        quat = myo.orientation

        strArray = [format(quat.x, '2.3f'), format(quat.y, '2.3f'), format(quat.z, '2.3f'), format(quat.w, '2.3f')]
        time.sleep(.01)
        # print("Euler: " + quaternionToEuler(str(format(w, '2.4f')),
        #                                     str(format(x, '2.4f')),
        #                                     str(format(y, '2.4f'),
        #
        #                                    str(format(z, '2.4f')))))
        arr = quaternionToEuler(quat.w,
                                quat.x,
                                quat.y,
                                quat.z)
        # str(arr)
        ard.write(str(arr).encode())
        # ard.write(arrayToStringWithMarker(strArray).encode())

        # print('Orientation:', format(quat.x,'2.4f'), format(quat.y,'2.4f'), format(quat.z,'2.4f'), format(quat.w,'2.4f'))

finally:
    hub.shutdown()  # !! crucial

