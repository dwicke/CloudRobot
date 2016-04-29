#!/usr/bin/env python

import cv2
import numpy as np
import socket
import zlib
import thread
import json
import sys
import select
import time
import random
import multiprocessing


def handler(sourcePort,imageBuffer):
    imageSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    imageSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    imageSock.bind(('0.0.0.0', sourcePort))
    
    prevID = -1

    while True:
        ready_socks, _, _ = select.select([imageSock], [], [], 0.05)
        if len(ready_socks) == 0:
            continue
        else:
            # we are getting something, put it into shared memory
            data, addr = self.sock.recvfrom(4096)
            try:
                decompData = zlib.decompress(data)
                #print 'the data %s' % (decompData)
                loc = decompData.find(',')
                imageID = decompData[:loc]
                if imageID > prevID:
                    prevID = imageID
                    #print 'image id %s' % (self.imageID)
                    decompData = decompData[loc+1:]
                    imageBuffer[0] = decompData
            except Exception as details:
                print 'could not decompress image stuffs error: %s' % (details)
                imageBuffer[0] = None


class VisualServoing(object):

    def __init__(self, sourceIP, sourcePort, destIP, destPort, taskName):

        print "Starting"
        self.vel_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.vel_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.vel_socket.bind(('0.0.0.0', destPort))
        data, self.robotClient = self.vel_socket.recvfrom(2048)


        print "visual servoing got from %s:%d robot: %s" % (self.robotClient[0], self.robotClient[1], data)
        self.vel_socket.sendto("connected", self.robotClient)

#       create the shared memory for image
        manager = Manager()
        self.imageBuffer = manager.list(range(1))
        
#       start the process for constantly grab image from socket
        self.process = multiprocessing.Process(target=handler, args=(sourcePort, self.imageBuffer))
        self.process.daemon = True
        self.process.start()


        self.prevFor = 0.0
        self.prevAng = 0.0
        self.HEIGHT = 240
        self.WIDTH = 320
        self.CHANNELS = 3
        self.MSGLEN = self.WIDTH*self.HEIGHT*self.CHANNELS
        self.BONDSMANPORT = 14000
        self.taskName = taskName
        self.probThresh = 0.65


    def doTask(self):
        myRan = random.random()
        print "random %f" % (myRan)
        if myRan < self.probThresh:
            print "///////////////sleeping!------------------>"
            return 0.0
            #time.sleep(.05)


        return self.visualServoingAction()


    def findBlob(self, frame):

        ## adapted from https://github.com/CarlosGS/GNBot/blob/master/Software/PreviousWork/OpenCV_tracking/BasicTests/test2.py


        thresh = cv2.erode(frame, None, iterations=2)
        #thresh = cv2.dilate(thresh, None, iterations=2)
        #thresh2 = thresh.copy()
        # find contours in the threshold image
        contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)


        #finding contour with maximum area and store it as best_cnt
        max_area = 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > max_area:
                max_area = area
                best_cnt = cnt

        #finding centroids of best_cnt and draw a circle there
        try:
            M = cv2.moments(best_cnt)
            cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
            #cv2.circle(frame,(cx,cy),5,255,-1)
            ###cx and cy is the center of the circle
            return cx, cy
            #return thresh2, frame, cx, cy
        except:
            return -1, -1
            #return thresh2, frame, -1, -1


    def processSocketImage(self):
        if self.imageBuffer == None:
            return False, None
        
        decompData = self.imageBuffer
        loc = decompData.find(',')
        self.imageTimestamp = decompData[:loc]
        #print 'image timestamp: %s' % (self.imageTimestamp)
        rcvimg = decompData[loc+1:]
        image = np.array(bytearray(rcvimg), dtype="uint8").reshape(self.HEIGHT, self.WIDTH)
    
        return True, image

#    def processSocketImage(self) :
#        #print 'Connected to server'
#
#        ready_socks,_,_ = select.select([self.sock], [], [], 0.3)
#        if len(ready_socks) == 0:
#            return False, None
#        data, addr = self.sock.recvfrom(4096)
#        # first decompress the data and split on newline
#        #print 'I got data! size from %s is: %d' % (addr[0], len(data))
#        rcvimg = None
#        try:
#            decompData = zlib.decompress(data)
#            #print 'the data %s' % (decompData)
#            loc = decompData.find(',')
#            self.imageID = decompData[:loc]
#            #print 'image id %s' % (self.imageID)
#            decompData = decompData[loc+1:]
#            loc = decompData.find(',')
#            self.imageTimestamp = decompData[:loc]
#            #print 'image timestamp: %s' % (self.imageTimestamp)
#            rcvimg = decompData[loc+1:]
#        except Exception as details:
#            print 'could not decompress image stuffs error: %s' % (details)
#            return False, None
#
#
#        # self.imageID = decompData[0]
#        # self.imageTimestamp = decompData[1]
#        # rcvimg = decompData[2]
#        # print str(self.imageID) + ' ' + str(self.imageTimestamp)
#
#        image = np.array(bytearray(rcvimg), dtype="uint8").reshape(self.HEIGHT,self.WIDTH)
#
#        return True, image

    ## units are mm/s degrees/s
#    def visualservo(self, blobx, bloby) :
#        forV = 0.0
#        angV = 0.0
#        if blobx == -1 :
#            return forV, angV
#
#        centerX = self.WIDTH / 2
#        if blobx < (centerX - 10) :
#            angV = 0.10
#            #print "setting turn left velocity"
#        elif blobx > (centerX + 10) :
#            angV = -0.10
#            #print "setting turn right velocity"
#        if bloby < self.HEIGHT - 15 :
#            forV = 0.1
#            #print "setting forward velocity"
#
#        #print '"%f"  "%f"' % (forV, angV)
#        return forV, angV


    def visualservo(self, blobx, bloby):
        forV = 0.0
        angV = 0.0
        if blobx == -1:
            return forV, angV

#       p controller for horizontal position
        centerX = self.WIDTH / 2
        angPGain = 0.1
        angError = blobx - centerX
        angV = -1.0 * angError * angPGain

#       p controller for vertical position
        forPGain = 0.1
        forError = self.HEIGHT - bloby - 50
        forV = forError * forPGain
            
        return forV, angV

    def visualServoingAction(self):
        starttime = time.time()
        success, image = self.processSocketImage()
        if success == False: # then I got a bad packet. must decide what to do now
            return 0.0
         #   return None
        #thresh, image, cx, cy = self.findBlob(image)
        cx, cy = self.findBlob(image)
        #print 'x = "%d" y = "%d"' % (cx, cy)
        #cv2.imshow("Image", image)
        #cv2.imshow("thresh", thresh)
        #cv2.waitKey(1)
        # ## units are mm/s degrees/s
        forwardVelocity, angularVelocity = self.visualservo(cx, cy)
        data = '%f, %f, %d, %f, %s' % (forwardVelocity, angularVelocity, int(self.imageID), float(self.imageTimestamp), self.taskName)
        #if self.prevFor != forwardVelocity or self.prevAng != angularVelocity:
            # need to reply since it is asking for it... otherwise not rewarded...
        self.prevFor = forwardVelocity
        self.prevAng = angularVelocity
        #print 'Sending %s to the robot' % (data)
        self.vel_socket.sendto(data, self.robotClient)
        endtime = time.time()
        print "id = %d total time = %f" %(int(self.imageID), endtime - starttime)
        return 1.0
