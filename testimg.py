#from cv2.cv import *
import cv2
import numpy as np
import socket
import zlib

vel_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 8052))
#sock.listen(1)
#conn, addr = sock.accept()
HEIGHT = 240
WIDTH = 320
CHANNELS = 3
MSGLEN = WIDTH*HEIGHT*CHANNELS

def myreceive():
        data, addr = sock.recvfrom(1024)
        return zlib.decompress(''.join(map(str, data)))
        # chunks = []
        # bytes_recd = 0
        # while bytes_recd < MSGLEN:
        #     chunk = conn.recv(min(MSGLEN - bytes_recd, 2048))
        #     if chunk == '':
        #         raise RuntimeError("socket connection broken")
        #     chunks.append(chunk)
        #     bytes_recd = bytes_recd + len(chunk)
        #     #print 'bytes read "%d" ' % (bytes_recd)
        # return ''.join(chunks)

def findBlob(frame):

    ## adapted from https://github.com/CarlosGS/GNBot/blob/master/Software/PreviousWork/OpenCV_tracking/BasicTests/test2.py
    # smooth it
    frame = cv2.blur(frame,(3,3))

    # convert to hsv and find range of colors
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    ORANGE_MIN = np.array([5, 50, 50],np.uint8)
    ORANGE_MAX = np.array([15, 255, 255],np.uint8)
    thresh = cv2.inRange(hsv,ORANGE_MIN, ORANGE_MAX)
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=2)
    #thresh = cv2.inRange(hsv,np.array((0, 80, 80)), np.array((20, 255, 255)))
    #thresh = cv2.inRange(hsv,np.array((15, 155, 255)), np.array((15, 255, 255)))
    #thresh = cv2.inRange(hsv,np.array((255, 128, 0)), np.array((255, 180, 100)))
    thresh2 = thresh.copy()



    # find contours in the threshold image
    contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)



    # circles = cv2.HoughCircles(thresh, cv2.cv.CV_HOUGH_GRADIENT, 1.2, 20)

    # max_r = 0
    # best_circ = (-1, -1)
    # if circles is not None:
    #     for (x, y, r) in circles:
    #         if r > max_r :
    #             max_r = r
    #             best_circ = (x, y, r)

    #     cv2.circle(frame,(best_circ[0], best_circ[1]), best_circ[2],255,-1)
    # return thresh2, frame, best_circ[0], best_circ[1]

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

    rcvimg = myreceive()
    print len(rcvimg)
    #image = np.array(bytearray(rcvimg), dtype="uint8").reshape(HEIGHT,WIDTH,CHANNELS)

    #print 'decode'
    #print image

    return rcvimg

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



while True:
    image = processSocketImage()
    ## if goAfterBounty() then


    # thresh, image, cx, cy = findBlob(image)
    # print 'x = "%d" y = "%d"' % (cx, cy)
    # cv2.imshow("Image", image)
    # cv2.imshow("thresh", thresh)
    # cv2.waitKey(1)
    # ## units are mm/s degrees/s
    # forwardVelocity, angularVelocity = visualservo(cx, cy)
    # data = '%f, %f' % (forwardVelocity, angularVelocity)
    # vel_socket.sendto(data, ("10.112.120.19", 15000))

