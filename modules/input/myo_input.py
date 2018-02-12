from threading import Thread
from myo import init, Hub, Feed
from decimal import *
from observable import Observable
import math

obs = Observable()

getcontext().prec = 4

init('sdk/myo.framework')
feed = Feed()
hub = Hub()
hub.run(1000, feed)

def getObservable():
    print("got observable")
    return obs

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

    return [X, Y, Z]

def main():
    #Repeating logic goes in here
    while True:
        try:
            myo = feed.wait_for_single_device(timeout=2.0)  # connecting to Myo
            if not myo:
                print("No Myo connected after 2 seconds")
            print("Connected to Myo")
            while hub.running and myo.connected:
                quat = myo.orientation
                arr = quaternionToEuler(quat.w,
                                        quat.x,
                                        quat.y,
                                        quat.z)
                (pose) = myo.pose.value
                obs.trigger('input', {'myo': arr , 'pose': pose })

        finally:
            hub.shutdown()  #!! crucial

        return

main_thread = Thread(target=main)
main_thread.setDaemon(True)
main_thread.start()
