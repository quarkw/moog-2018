#!/usr/bin/env python
from myo import init, Hub, Feed
from decimal import *

getcontext().prec = 4

init()
feed = Feed()
hub = Hub()
hub.run(1000, feed)

try:
    myo = feed.wait_for_single_device(timeout=2.0)
    if not myo:
        print("No Myo connected after 2 seconds")
        print("Hello, Myo!")
    while hub.running and myo.connected:
        quat = myo.orientation
        print('Orientation:', format(quat.x,'2.4f'), format(quat.y,'2.4f'), format(quat.z,'2.4f'), format(quat.w,'2.4f'))
finally:
    hub.shutdown()  # !! crucial
