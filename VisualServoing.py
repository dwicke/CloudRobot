#!/usr/bin/env python

import cv2
import numpy as np
import socket
import zlib
import thread
import json
import sys

class VisualServoing(object):


    HEIGHT = 240
    WIDTH = 320
    CHANNELS = 3
    MSGLEN = WIDTH*HEIGHT*CHANNELS
    BONDSMANPORT = 14000


    def __init__(self, sourceIP, sourcePort, destIP, destPort):
        self.vel_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((sourceIP, sourcePort))
        self.destIP = destIP
        self.destPort = destPort
        self.prevFor = 0.0
        self.prevAng = 0.0

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
        data, addr = self.sock.recvfrom(1024)
        # first decompress the data and split on newline
        decompData = zlib.decompress(data).split( )
        self.imageID = decompData[0]
        self.imageTimestamp = decompData[1]
        rcvimg = decompData[2]


        image = np.array(bytearray(rcvimg), dtype="uint8").reshape(HEIGHT,WIDTH)

        return image

    ## units are mm/s degrees/s
    def visualservo(self, blobx, bloby) :
        forV = 0.0
        angV = 0.0
        if blobx == -1 :
            return forV, angV

        centerX = WIDTH / 2
        if blobx < (centerX - 10) :
            angV = 0.10
            print "setting turn left velocity"
        elif blobx > (centerX + 10) :
            angV = -0.10
            print "setting turn right velocity"
        elif bloby < HEIGHT - 15 :
            forV = 0.1
            print "setting forward velocity"

        print '"%f"  "%f"' % (forV, angV)
        return forV, angV




    def visualServoingAction(self):
        image = processSocketImage()
        thresh, image, cx, cy = findBlob(image)
        print 'x = "%d" y = "%d"' % (cx, cy)
        cv2.imshow("Image", image)
        cv2.imshow("thresh", thresh)
        cv2.waitKey(1)
        # ## units are mm/s degrees/s
        forwardVelocity, angularVelocity = visualservo(cx, cy)
        data = '%f, %f, %f, %f' % (forwardVelocity, angularVelocity, self.imageID, self.imageTimestamp)
        if self.prevFor != forwardVelocity or self.prevAng != angularVelocity:
            self.prevFor = forwardVelocity
            self.prevAng = angularVelocity
            self.vel_socket.sendto(data, (self.destIP, self.destPort))
