#!/usr/bin/env python

from ConnectionManager import ConnectionManager
udpCon = ConnectionManager('udp')
udpCon.addClient('localhost', 9000)
udpCon.send('HIIH I am udp')


udpCon = ConnectionManager('tcp')
udpCon.addClient('localhost', 9001)
udpCon.send('HIIH i am tcp yo')
