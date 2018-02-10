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
    print("Connected to Myo and Arduino")
    if not myo:
        print("No Myo connected after 2 seconds")
    while hub.running and myo.connected:
        quat = myo.orientation
        time.sleep(.01)

        arr = quaternionToEuler(quat.w,
                                quat.x,
                                quat.y,
                                quat.z)
        ard.write(str(arr).encode())


finally:
    hub.shutdown()  # !! crucial

