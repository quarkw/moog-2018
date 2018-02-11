from threading import Thread

import serial
import time
import re
from observable import Observable

obs = Observable()

def getObservable():
    print("got observable")
    return obs

connected = False

serial_port = serial.Serial('/dev/cu.usbmodem14111', timeout=2, baudrate=9600)

time.sleep(2)

def getSerialPort():
    return serial_port


def trigger(data_str):
    obs.trigger('input',{'soft_pot': data_str})

def read_from_port(ser):
    global connected
    while not connected:
        #serin = ser.read()
        connected = True

        while True:
            if (ser.inWaiting() > 0):
                try:
                    data_str = str(ser.readline(ser.inWaiting()).decode('ascii'))
                    data_str1 = re.sub("\s", "", data_str)
                    if data_str1 == "":
                        data_str1 = "0"
                    trigger(int(data_str1))
                except:
                    print("Arduino received: " + data_str)


thread = Thread(target=read_from_port, args=(serial_port,))
thread.start()
