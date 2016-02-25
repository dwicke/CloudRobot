#!/usr/bin/env python


class DataCollector(object):

    def __init__(self):
        self.collectedData = {}

    def addPoint(self, setName, point):
        if setName not in self.collectedData:
            self.collectedData[setName] = []
        self.collectedData[setName].append(point)

    def writeData(self):
        '''
        writes all data
        '''
        for k in self.collectedData.keys()
            thefile = open( k + ".dat", "wb" )
            i = 0
            for item in self.collectedData[k]:
                thefile.write("%d,%s\n" % (i, str(item)))
                i += 1
            thefile.close()
    def deleteSet(setName):
        del self.collectedData[setName]
