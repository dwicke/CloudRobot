class QTable(object):
    def __init__(self, numStates, numActions, alpha):
        self.numStates = numStates
        self.numActions = numActions
        self.alpha = alpha
        self.oneMinusAlpha = 1 - alpha
        self.qtable = [ [ 1 for i in range(numActions) ] for j in range(numStates) ]

    def update(self, state, action, reward):
        self.qtable[state][action] = self.oneMinusAlpha * self.qtable[state][action] + self.alpha * reward;

    def getQValue(self, state, action):
        return self.qtable[state][action]
