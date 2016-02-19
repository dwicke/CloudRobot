#!/usr/bin/env python

import socket
import thread
import json
from VisualServoing import VisualServoing
from BountyHunterLearner import BountyHunterLearner


def bondsmanListener():
    bondSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bondSock.bind(('0.0.0.0', BONDSMANPORT))
    while True:
        print 'hi'
        data, addr = bondSock.recvfrom(60000)
        ## check if success or task
        print data
        listData = json.loads(data)
        print listData[0]
        ## if success then learn

        ## if task then add it to the learning function ComplexP
        ## and add it to the task list



def getTask():
    ## in the future will querry the learning algorithm
    ## and the curent tasks and the tasks will have a
    ## function associated with them such as visualServoingAction
    return visualServoingAction

try:
    thread.start_new_thread(bondsmanListener,())
except:
   print "Error: unable to start thread"

while True:
    task = getTask()
    #task()

