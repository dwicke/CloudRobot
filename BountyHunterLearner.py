'''
    This class can be used as both Complex(P,R) and Simple(P,R) depending on
    how its used.
'''
class BountyHunterLearner(object):
    def __init__(self, alphaT, alphaP, oneUpdateGamma, hasOneUpdate, ):
        self.TTable = QTable(alphaT, oneUpdateGamma, 1)
        self.PTable = QTable(alphaP, oneUpdateGamma, 1)
        self.hasOneUpdate = hasOneUpdate

    ## need the time it took to complete the task, who else worked
    ## on the same task, and the reward (1 if I won 0 otherwise)
    def learn(self, task, roundtriptime, agentsWorking, reward):
        if reward == 1:
            self.TTable.update(task, 0, roundtriptime)
            for agent in agentsWorking:
                self.PTable.update(task, agent, reward)

        else:
            self.PTable.update(task, agent, reward)

        if self.hasOneUpdate == True:
            self.PTable.oneupdate()

    ## tasks is a list of tasks [{'name': 'task_name', 'cur_bounty': <val>, }, ...]
    ## return task name i'm picking
    def pickTask(self, tasks):

