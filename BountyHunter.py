#!/usr/bin/env python

import socket
import thread
import json
import threading
from VisualServoing import VisualServoing
from BountyHunterLearner import BountyHunterLearner
from ConnectionManager import ConnectionManager

## in the future can dynamically load new task handlers
## http://stackoverflow.com/questions/547829/how-to-dynamically-load-a-python-class



class DoNothing(object):
    def __init__(self):
        return None
    def doTask(self):
        return None

class BountyHunter(object):

    def __init__(self):
        self.BONDSMANPORT = 14000
        #self.taskLock = threading.Lock()
        self.taskSet = {}
        self.taskSet['DoNothing'] = {'handler':DoNothing(), 'name': 'DoNothing', 'initBounty': 10.0, 'bountyRate': 1.0, 'deadline': 30.0}

        ## in the future the task handlers will be dynamically
        ## loaded and refreshed to  make sure the latest and
        ## onewest available...
        self.taskHandlers = {}
        self.taskHandlers['default'] = DoNothing
        self.taskHandlers['visualServoing'] = VisualServoing
        ## create the learner
        #alphaT, alphaP, oneUpdateGamma, hasOneUpdate, epsilonChooseRandomTask
        self.bountyLearner = BountyHunterLearner(0.1,0.2,0.001,True, 0.002)
        self.myIP = str([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])

        self.bondSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bondSock.setblocking(0)
        self.bondSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.bondSock.bind(('0.0.0.0', self.BONDSMANPORT))

        ## start up the listener thread for new tasks
        # try:
        #     thread.start_new_thread(self.bondsmanListener,())
        # except:
        #    print "Error: unable to start thread"

        # hunt bounties forever....
        while True:
            task = self.getTask()
            task['handler'].doTask()
            self.bondsmanListener()


    def bondsmanRecv(self):

        ready = select.select([self.bondSock], [], [], 0.03)
        if not ready[0]:
            return None
        data, addr = bondSock.recvfrom(32768)
        ## check if success or task
        print data
        listData = json.loads(data)
        if listData[0] == 'task':
            print listData[1]
            ## if task then add it to the learning function?
            ## and add it to the task list
            if listData[1] + '-' + addr[0] not in self.taskSet:
                # so if I can actually do the task then add the task.
                if listData[1] in self.taskHandlers:
                    #self.taskLock.acquire()
                    self.taskSet[listData[1] + '-' + addr[0]] = {'handler':self.taskHandlers[listData[1]](addr[0], listData[6], addr[0], listData[7], listData[1]), 'name': listData[1], 'initBounty': listData[3], 'bountyRate': listData[4], 'deadline': listData[5], 'hunters': listData[2]}
                    #self.taskLock.release()
        else:
            print 'Recv a success message for task %s total time = %s' % (listData[1], listData[4])
            if listData[3] == self.myIP:
                ## Then I won!!
                self.bountyLearner.learn(listData[1] + '-' + addr[0], float(listData[4]), 0, 1)
            else:
                self.bountyLearner.learn(listData[1] + '-' + addr[0], float(listData[4]), 0, 0)

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


        while True:
            print 'hi'
            ## addr is ('ipaddress', port)





    def getTask(self):
        ## in the future will querry the learning algorithm
        ## and the curent tasks and the tasks will have a
        ## function associated with them such as visualServoingAction
        #self.taskLock.acquire()
        taskRunner = self.bountyLearner.getTask(self.taskSet)
        #self.taskLock.release()
        return taskRunner


# do tasks...
bme = BountyHunter()
