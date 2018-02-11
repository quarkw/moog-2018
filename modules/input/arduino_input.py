from threading import Thread

import serial
import time
from observable import Observable

obs = Observable()

def getObservable():
    print("got observable")
    return obs

connected = False

serial_port = serial.Serial('/dev/cu.usbmodem14111', timeout=2, baudrate=115200)
time.sleep(2)

def trigger(data_str):
    obs.trigger('input',{'soft_pot': data_str})

def read_from_port(ser):
    global connected
    while not connected:
        #serin = ser.read()
        connected = True

        while True:
            if (ser.inWaiting() > 0):
                data_str = ser.readline(ser.inWaiting()).decode('ascii')
                trigger(data_str)

thread = Thread(target=read_from_port, args=(serial_port,))
thread.start()
