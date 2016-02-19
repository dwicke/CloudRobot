#!/usr/bin/env python

import socket
import thread
import json
from VisualServoing import VisualServoing
from BountyHunterLearner import BountyHunterLearner
## in the future can dynamically load new task handlers
## http://stackoverflow.com/questions/547829/how-to-dynamically-load-a-python-class



class DoNothing(object):
    def __init__(self):
        return ()
    def doTask(self):
        return ()

class BountyHunter(object):

    def __init__(self):
        self.BONDSMANPORT = 14000
        self.taskLock = Lock()
        self.taskSet = {}
        self.taskSet['DoNothing'] = {'handler':DoNothing, 'name': 'DoNothing', 'initBounty': 100.0, 'bountyRate': 1.0, 'deadline': 30.0}

        ## in the future the task handlers will be dynamically
        ## loaded and refreshed to  make sure the latest and
        ## onewest available...
        self.taskHandlers = {}
        self.taskHandlers['default'] = DoNothing
        self.taskHandlers['visualServoing'] = VisualServoing
        ## create the learner
        #alphaT, alphaP, oneUpdateGamma, hasOneUpdate, epsilonChooseRandomTask
        self.bountyLearner = BountyHunterLearner(0.1,0.2,0.001,True, 0.002)

        ## start up the listener thread for new tasks
        try:
            thread.start_new_thread(self.bondsmanListener,())
        except:
           print "Error: unable to start thread"

        # hunt bounties forever....
        while True:
            task = self.getTask()
            task['handler'].doTask()

    def bondsmanListener(self):
        '''
            0 string msgType (task/success)
            1 string taskName
            2 string[] bountyHunters
            3 float64 initialBounty
            4 float64 bountyRate
            5 float64 deadline
            6 uint32 inputPort
            7 uint32 outputPort
        '''
        bondSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        bondSock.bind(('0.0.0.0', self.BONDSMANPORT))
        while True:
            print 'hi'
            ## addr is ('ipaddress', port)
            data, addr = bondSock.recvfrom(32768)
            ## check if success or task
            print data
            listData = json.loads(data)
            if listData[0] == 'task':
                print listData[1]
                ## if task then add it to the learning function?
                ## and add it to the task list
                if listData[1] + '-' + addr[0] not in taskSet:
                    # so if I can actually do the task then add the task.
                    if listData[1] in taskHandlers:
                        self.taskLock.aquire()
                        taskSet[listData[1] + '-' + addr[0]] = {'handler':taskHandlers[listData[1]](addr[0], listData[6], addr[0], listData[7]), 'name': listData[1], 'initBounty': listData[3], 'bountyRate': listData[4], 'deadline': listData[5], 'hunters': listData[2]}
                        self.taskLock.release()
            else:
                print listData[1]
                ## if success packet then learn!!
                ## first check if i did do the task
               # if listData[1] + '-' + addr[0] in taskSet:
                 #   if taskSet[listData[1] + '-' + addr[0]]['handler'].




    def getTask(self):
        ## in the future will querry the learning algorithm
        ## and the curent tasks and the tasks will have a
        ## function associated with them such as visualServoingAction
        self.taskLock.aquire()
        taskRunner = self.bountyLearner.getTask(self.taskSet)
        self.taskLock.release()
        return taskRunner


# do tasks...
bme = BountyHunter()
