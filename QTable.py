#!/usr/bin/env python

class QTable(object):
    def __init__(self, alpha, gamma, defaultValue):
        self.alpha = alpha
        self.oneMinusAlpha = 1 - alpha
        self.gamma = gamma
        self.oneMinusGamma = 1 - gamma
        self.defaultValue
        self.qtable = {}

    def update(self, state, action, reward):
        if state not in self.qtable
            self.qtable[state] = {}
        if action not in self.qtable[state]
            self.qtable[state][action] = self.defaultValue

        self.qtable[state][action] = self.oneMinusAlpha * self.qtable[state][action] + self.alpha * reward;

    def getQValue(self, state, action):
        return self.qtable[state][action]

    def oneUpdate(self):
        self.qtable = {k: {k2: v2*self.oneMinusGamma + self.gamma for k2, v2 in v.items()} for k, v in self.qtable.items()}
