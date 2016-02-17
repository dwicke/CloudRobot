class ComplexP(object):
    def __init__(self, numTaskClasses, numAgents, alphaT, alphaP):
        self.numTaskClasses = numTaskClasses
        self.numAgents = numAgents
        self.TTable = QTable(numTaskClasses, 1, alphaT)
        self.PTable = QTable(numTaskClasses, numAgents, alphaP)


    ## need the time it took to complete the task, who else worked
    ## on the same task, and the reward (1 if I won 0 otherwise)
    def learn(self, taskID, roundtriptime, agentsWorking, reward):
        if reward == 1:
            self.TTable.update(taskID, 0, roundtriptime)
            for

    def pickTask(self):

