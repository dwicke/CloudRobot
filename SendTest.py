#!/usr/bin/env python
from ConnectionManager import ConnectionManager




udpCon = ConnectionManager('udp', )
udpCon.addClient('localhost', 9000)
udpCon.send('HIIH I am udp')
udpCon.recv()
# tcpCon = ConnectionManager('tcp')
# tcpCon.addClient('localhost', 9001)
# tcpCon.send('HIIH i am tcp yo')
# tcpCon.recv()
