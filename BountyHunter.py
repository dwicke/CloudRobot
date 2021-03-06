#!/usr/bin/env python

import socket
import select
import json
from VisualServoing import VisualServoing
from BountyHunterLearner import BountyHunterLearner
from DataCollector import DataCollector

## in the future can dynamically load new task handlers
## http://stackoverflow.com/questions/547829/how-to-dynamically-load-a-python-class



class DoNothing(object):
    def __init__(self):
        return None
    def doTask(self):
        return 0.0

class BountyHunter(object):

    def __init__(self):
        self.BONDSMANPORT = 14000
        self.taskSet = {}
        self.taskSet['DoNothing'] = {'handler':DoNothing(), 'name': 'DoNothing', 'initBounty': 0.65, 'bountyRate': 0.0, 'deadline': 30.0, 'currentBounty': 0.65}

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
        self.bondSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.bondSock.bind(('0.0.0.0', self.BONDSMANPORT))
        self.timesSent = 1.0
        self.datacollector = DataCollector()
        self.currentHZ = 5
        self.timesSucc = 0.0
        self.doneSim = False
        self.currentset = ''
        while self.doneSim == False:
            self.curtask = self.bountyLearner.getTask(self.taskSet)
            #print 'current bounty rate for task %s is %f' % (self.curtask['name'], self.curtask['bountyRate'])
            for task in self.taskSet.values():
                task['currentBounty'] += task['bountyRate']
            self.timesSent += self.curtask['handler'].doTask()
            self.doneSim = self.bondsmanRecv()


    def bondsmanRecv(self):
        '''
            Task MSG
            0 string msgType (task)
            1 string taskName
            2 string[] bountyHunters
            3 float64 initialBounty
            4 float64 bountyRate
            5 float64 deadline
            6 uint32 inputPort
            7 uint32 outputPort

            Succ MSG
            0 string msgType (success)
            1 string task
            2 uint32 taskID
            3 string winnerIP
            4 float64 totalTime
            5 uint32 succCount
            6 uint32 recvCount
        '''
        ready = select.select([self.bondSock], [], [], 0.03)
        if not ready[0]:
            return False
        data, addr = self.bondSock.recvfrom(32768)
        ## check if success or task
        #print data
        listData = json.loads(data)
        if listData[0] == 'task':
            print listData[1]
            ## if task then add it to the learning function?
            ## and add it to the task list
            if listData[1] + '-' + addr[0] not in self.taskSet:
                # so if I can actually do the task then add the task.
                if listData[1] in self.taskHandlers:
                    self.taskSet[listData[1] + '-' + addr[0]] = {'handler':self.taskHandlers[listData[1]](addr[0], listData[6], addr[0], listData[7], listData[1]), 'name': listData[1], 'initBounty': listData[3], 'bountyRate': listData[4], 'deadline': listData[5], 'hunters': listData[2], 'currentBounty': listData[3]}
            else:
                # we already have that task
                self.taskSet[listData[1] + '-' + addr[0]]['deadline'] = listData[5]
                self.currentDataset = str(listData[5]) + 'hzData_'+ self.myIP
        elif listData[0] == 'success':

            if listData[2] == -1:
                # THEN WE ARE FINISHED
                self.datacollector.writeData()
                return True
            #print 'Recv a success message for task %s total time = %s SuccCount = %d' % (listData[1], listData[4], listData[5])
            totalTime = float(listData[4]) * 1000.0 # convert to milliseconds
            self.curtask['currentBounty'] = self.curtask['initBounty']


            if listData[5] == 1:
                print 'list data was 1!'
                self.currentHZ += 5
                self.timesSent = 1.0 # reset.
                self.timesSucc = 0.0
                self.currentset = 'bountyhunter-' + self.myIP + '-' + str(self.currentHZ)


            if listData[3] == self.myIP:
                ## Then I won!!
                self.bountyLearner.learn(listData[1] + '-' + addr[0], totalTime, 0, 1)
                self.timesSucc += 1.0
            else:
                self.bountyLearner.learn(listData[1] + '-' + addr[0], totalTime, 0, 0)


            if self.curtask['name'] == 'DoNothing':
                self.datacollector.addPoint(self.currentset, (int(listData[5]), -1.0))
            else:
                self.datacollector.addPoint(self.currentset, (int(listData[5]), self.timesSucc / self.timesSent))
        else:
            print 'ERROR unexpected message: %s' % (data)
        return False

# do tasks...
bme = BountyHunter()
