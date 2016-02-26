#!/usr/bin/env python
import random
from QTable import QTable
'''
    This class can be used as both Complex(P,R) and Simple(P,R) depending on
    how its used.
'''
class BountyHunterLearner(object):
    def __init__(self, alphaT, alphaP, oneUpdateGamma, hasOneUpdate, epsilonChooseRandomTask, tInit = 1, pInit = 1):
        self.TTable = QTable(alphaT, oneUpdateGamma, tInit)
        self.PTable = QTable(alphaP, oneUpdateGamma, pInit)
        self.hasOneUpdate = hasOneUpdate
        self.epsilonChooseRandomTask = epsilonChooseRandomTask
        self.lastTask = ''
        self.lastI = 0

    ## need the time it took to complete the task, who else worked
    ## on the same task, and the reward (1 if I won 0 otherwise)
    def learn(self, task, roundtriptime, agentsWorking, reward):
        if reward == 1:
            self.TTable.update(task, 0, roundtriptime)
            #for agent in agentsWorking:
            self.PTable.update(task, 0, reward)

        else:
            #self.PTable.update(task, agent, reward)
            self.PTable.update(task, 0, reward)

        if self.hasOneUpdate == True:
            self.PTable.oneUpdate()

    ## tasks is a list of tasks [{'name': 'task_name', 'cur_bounty': <val>, }, ...]
    ## return task name i'm picking
    def getTask(self, tasks):
        if self.epsilonChooseRandomTask > random.random():
            # then pick a random task
            taskName = random.choice(tasks.keys())
            print 'Picked random task %s' % (taskName)
            lastTask = taskName
            return tasks[taskName]
        else:
            # pick a task regularly
            #for k,v in tasks:
            bestTask = None
            maxI = -1
            for k, v in tasks.iteritems():

                T = self.TTable.getQValue(k, 0)
                P = self.PTable.getQValue(k, 0)
                I = (v['currentBounty']/T)*P
                #print 'The currentBounty = %f and I = %f T = %f P = %f for task %s' % (v['currentBounty'], I, T, P, k)
                if I > maxI:
                    maxI = I
                    bestTask = v

            if self.lastTask != bestTask['name'] or maxI != self.lastI:
                self.lastTask = bestTask['name']
                self.lastI = maxI
                #print 'Picked specific task %s with I = %f' % (bestTask['name'], maxI)
            return bestTask

