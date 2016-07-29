#!/usr/bin/env python

import ach
from ctypes import *
from urllib2 import urlopen
import cv2
import numpy as np
import zlib

class TaskData(Structure):
    _fields_ = [('id', c_double),
                ('img', c_char_p)]

class VelDat(Structure):
    _fields_ = [('forwardVelocity', c_double),
                ('angularVelocity', c_double),
                ('id', c_double)]

HEIGHT = 240
WIDTH = 320



my_ip = urlopen('http://ip.42.pl/raw').read()
print("myip = " + my_ip)
## connect to the channels
recvTaskChannel = ach.Channel(my_ip.replace(".", "").replace("\n", "") + "VSTaskImg")
recvTaskChannel.chmod(0666) ## set so the robot can connect
recvTaskChannel.flush() ## clear old stuff out

sendRespChannel = ach.Channel(my_ip.replace(".", "").replace("\n", "") + "VSResp")
sendRespChannel.chmod(0666) ## set so the robot can connect
sendRespChannel.flush() ## clear old stuff out

veldat = VelDat()
veldat.forwardVelocity = 0.1
veldat.angularVelocity = 0.0
veldat.id = 1.0
taskdat = bytearray(320*240*3)
print("waiting for task data...")
## now
while True:
        recvTaskChannel.get(taskdat, wait=True, last=True)
        sendRespChannel.put(veldat)
