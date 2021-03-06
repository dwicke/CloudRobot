#!/usr/bin/env python

import cv2
import numpy as np
import socket
import zlib
import thread
import json
import sys

class VisualServoing(object):





    def __init__(self, sourceIP, sourcePort, destIP, destPort, taskName):

        ## image conn
        self.sock, self.sockAddr = self.tcpConnection('', sourcePort)
        ## velocity conn
        self.vel_socket, self.velAddr = self.tcpConnection('', destPort)


        self.destIP = destIP
        self.destPort = destPort
        self.prevFor = 0.0
        self.prevAng = 0.0
        self.HEIGHT = 240
        self.WIDTH = 320
        self.CHANNELS = 3
        self.MSGLEN = self.WIDTH*self.HEIGHT*self.CHANNELS
        self.taskName = taskName

    def tcpConnection(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, port))
        sock.listen(1)
        return sock.accept()

    def doTask(self):
        self.visualServoingAction()


    def findBlob(self, frame):

        ## adapted from https://github.com/CarlosGS/GNBot/blob/master/Software/PreviousWork/OpenCV_tracking/BasicTests/test2.py


        thresh = cv2.erode(frame, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=2)
        thresh2 = thresh.copy()
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
            cv2.circle(frame,(cx,cy),5,255,-1)
            ###cx and cy is the center of the circle
            return thresh2, frame, cx, cy
        except:
            return thresh2, frame, -1, -1




    def processSocketImage(self) :
        #print 'Connected to server'
        data, addr = self.sock.recvfrom(2048)
        # first decompress the data and split on newline
        try:
            decompData = zlib.decompress(data).split( )
        except Exception as details:
            print 'could not decompress image stuffs error: %s' % (details)
            return None
        self.imageID = decompData[0]
        self.imageTimestamp = decompData[1]
        rcvimg = decompData[2]
        print str(self.imageID) + ' ' + str(self.imageTimestamp)

        image = np.array(bytearray(rcvimg), dtype="uint8").reshape(self.HEIGHT,self.WIDTH)

        return image

    ## units are mm/s degrees/s
    def visualservo(self, blobx, bloby) :
        forV = 0.0
        angV = 0.0
        if blobx == -1 :
            return forV, angV

        centerX = self.WIDTH / 2
        if blobx < (centerX - 10) :
            angV = 0.10
            print "setting turn left velocity"
        elif blobx > (centerX + 10) :
            angV = -0.10
            print "setting turn right velocity"
        elif bloby < self.HEIGHT - 15 :
            forV = 0.1
            print "setting forward velocity"

        print '"%f"  "%f"' % (forV, angV)
        return forV, angV




    def visualServoingAction(self):
        image = self.processSocketImage()
        if image == None: # then I got a bad packet. must decide what to do now
            return None
        thresh, image, cx, cy = self.findBlob(image)
        print 'x = "%d" y = "%d"' % (cx, cy)
        cv2.imshow("Image", image)
        cv2.imshow("thresh", thresh)
        cv2.waitKey(1)
        # ## units are mm/s degrees/s
        forwardVelocity, angularVelocity = self.visualservo(cx, cy)
        data = '%f, %f, %d, %f, %s' % (forwardVelocity, angularVelocity, int(self.imageID), float(self.imageTimestamp), self.taskName)
        if self.prevFor != forwardVelocity or self.prevAng != angularVelocity:
            self.prevFor = forwardVelocity
            self.prevAng = angularVelocity
            self.vel_socket.sendto(data, (self.destIP, self.destPort))
