#from cv2.cv import *
import cv2
import numpy as np
import socket
import zlib
import thread
import json
import sys

vel_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 8052))
#sock.listen(1)
#conn, addr = sock.accept()
HEIGHT = 240
WIDTH = 320
CHANNELS = 3
MSGLEN = WIDTH*HEIGHT*CHANNELS
BONDSMANPORT = 14000

def findBlob(frame):

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




def processSocketImage() :
    #print 'Connected to server'
    data, addr = sock.recvfrom(1024)
    rcvimg = zlib.decompress(data)

    image = np.array(bytearray(rcvimg), dtype="uint8").reshape(HEIGHT,WIDTH)

    return image

## units are mm/s degrees/s
def visualservo(blobx, bloby) :
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


def bondsmanListener():
    bondSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bondSock.bind(('0.0.0.0', BONDSMANPORT))
    while True:
        print 'hi'
        data, addr = bondSock.recvfrom(60000)
        ## check if success or task
        print data
        listData = json.loads(data)
        print listData[0]
        ## if success then learn

        ## if task then add it to the learning function ComplexP
        ## and add it to the task list


prevFor = 0.0
prevAng = 0.0

try:
    thread.start_new_thread(bondsmanListener,())
except:
   print "Error: unable to start thread"

while True:

    ## if goAfterBounty():

    image = processSocketImage()
    thresh, image, cx, cy = findBlob(image)
    print 'x = "%d" y = "%d"' % (cx, cy)
    cv2.imshow("Image", image)
    cv2.imshow("thresh", thresh)
    cv2.waitKey(1)
    # ## units are mm/s degrees/s
    forwardVelocity, angularVelocity = visualservo(cx, cy)
    data = '%f, %f' % (forwardVelocity, angularVelocity)
    if prevFor != forwardVelocity or prevAng != angularVelocity:
        prevFor = forwardVelocity
        prevAng = angularVelocity
        vel_socket.sendto(data, ("10.112.120.19", 15000))

