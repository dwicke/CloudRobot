#from cv2.cv import *
import cv2
import numpy as np
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('0.0.0.0', 8052))
sock.listen(1)
conn, addr = sock.accept()
HEIGHT = 240
WIDTH = 320
CHANNELS = 3
MSGLEN = WIDTH*HEIGHT*CHANNELS

def myreceive():
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = conn.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == '':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
            #print 'bytes read "%d" ' % (bytes_recd)
        return ''.join(chunks)

def findBlob(frame):

    ## adapted from https://github.com/CarlosGS/GNBot/blob/master/Software/PreviousWork/OpenCV_tracking/BasicTests/test2.py
    # smooth it
    frame = cv2.blur(frame,(3,3))

    # convert to hsv and find range of colors
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    thresh = cv2.inRange(hsv,np.array((0, 80, 80)), np.array((20, 255, 255)))
    #thresh = cv2.inRange(hsv,np.array((255, 128, 0)), np.array((255, 180, 100)))
    thresh2 = thresh.copy()

    # find contours in the threshold image
    contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    # finding contour with maximum area and store it as best_cnt
    max_area = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            best_cnt = cnt

    # finding centroids of best_cnt and draw a circle there
    try:
        M = cv2.moments(best_cnt)
        cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
        cv2.circle(frame,(cx,cy),5,255,-1)
        ###cx and cy is the center of the circle
        return thresh2, frame, cx, cy
    except:
        return thresh2, frame, 0, 0




def processSocketImage() :
    #print 'Connected to server'

    rcvimg = myreceive()
    image = np.array(bytearray(rcvimg), dtype="uint8").reshape(HEIGHT,WIDTH,CHANNELS)

    #print 'decode'
    #print image

    return image

## units are mm/s degrees/s
def visualservo(blobx, bloby) :
    return 0, 0

while True:
    image = processSocketImage()
    ## if goAfterBounty() then
    thresh, image, cx, cy = findBlob(image)
    cv2.imshow("Image", image)
    cv2.imshow("thresh", thresh)
    cv2.waitKey(1)
    ## units are mm/s degrees/s
    forwardVelocity, angularVelocity = visualservo(cx, cy)
    ## sock.send servo data back

