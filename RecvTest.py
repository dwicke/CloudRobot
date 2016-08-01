#!/usr/bin/env python
import time
from ConnectionManager import ConnectionManager


# udpCon = ConnectionManager('udp')
# udpCon.buildServer(9000)
# udpCon.recv()
# time.sleep(1)
# udpCon.send('hi', '127.0.0.1', 9000)

tcpCon = ConnectionManager('tcp')
tcpCon.buildServer(9001)
re = tcpCon.recv()

print(re)
print(len(re[0][0]))
time.sleep(2)
tcpCon.send('hi')




