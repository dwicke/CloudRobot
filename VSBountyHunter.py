#!/usr/bin/env python

import ach
from ctypes import *
from urllib2 import urlopen

class TaskData(Structure):
    _fields_ = [('id', c_double),
                ('img', c_char_p)]

class VelDat(Structure):
    _fields_ = [('forwardVelocity', c_double),
                ('angularVelocity', c_double),
                ('id', c_double)]


my_ip = urlopen('http://ip.42.pl/raw').read()

## connect to the channels
recvTaskChannel = ach.Channel(my_ip + "-VSTaskImg")
recvTaskChannel.chmod(0666) ## set so the robot can connect
recvTaskChannel.flush() ## clear old stuff out

sendRespChannel = ach.Channel(my_ip + "-VSResp")
sendRespChannel.chmod(0666) ## set so the robot can connect
sendRespChannel.flush() ## clear old stuff out


## now
while True:
    taskdat = TaskData()
    c.get( taskdat, wait=True, last=True )
    cx, cy = self.findBlob(np.array(bytearray(taskdat.img), dtype="uint8").reshape(self.HEIGHT, self.WIDTH))

    forwardVelocity, angularVelocity = self.visualservo(cx, cy)
    veldat = VelDat()
    veldat.forwardVelocity = forwardVelocity
    veldat.angularVelocity = angularVelocity
    veldat.id = taskdat.id

    sendRespChannel.put(veldat)


def visualservo(blobx, bloby):
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

def findBlob(frame):

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
