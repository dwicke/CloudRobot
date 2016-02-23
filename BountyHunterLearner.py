#!/usr/bin/env python
import random
from QTable import QTable
'''
    This class can be used as both Complex(P,R) and Simple(P,R) depending on
    how its used.
'''
class BountyHunterLearner(object):
    def __init__(self, alphaT, alphaP, oneUpdateGamma, hasOneUpdate, epsilonChooseRandomTask):
        self.TTable = QTable(alphaT, oneUpdateGamma, 1)
        self.PTable = QTable(alphaP, oneUpdateGamma, 1)
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
                I = (v['initBounty']/self.TTable.getQValue(k, 0))*self.PTable.getQValue(k, 0)
                if I > maxI:
                    maxI = I
                    bestTask = v

            if self.lastTask != bestTask['name'] or maxI != self.lastI:
                self.lastTask = bestTask['name']
                self.lastI = maxI
                print 'Picked specific task %s with I = %d' % (bestTask['name'], maxI)
            return bestTask

