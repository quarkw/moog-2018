# #!/usr/bin/env/python

import serial
import time
import random

for x in range(0, 1):
    y = random.randint(1, 255)
    y2 = random.randint(1, 255)
    y3 = random.randint(1, 255)
    y4 = random.randint(1, 255)
    y5 = random.randint(1, 255)
    y6 = random.randint(1, 255)

# strArray = [255, 255, 255, 255, 255, 255]
strArray = [y, y2, y3, y4, y5, y6]
print(strArray)


def arrayToStringWithMarker(array):
    return "<" + str(array) + ">"


try:
    arrayToStringWithMarker(strArray)
    print("trying to connect")
    ard = serial.Serial('/dev/cu.usbmodem14311', timeout=2, baudrate=115200)
    time.sleep(2)
    # ard.write(b'4')
    print("connected to arduino\n")
    while True:
        print("About to sleep")
        time.sleep(.01)
        print("Finished sleeping; about to write")
        ar = arrayToStringWithMarker(strArray)
        print("ar: " + ar)
        ard.write(ar)
        # ard.write(arrayToStringWithMarker(strArray))
        # ard.write("<" + str(strArray) + " " + str(counter) + ">")

except:
    print("Failed...")

