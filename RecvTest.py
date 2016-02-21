#!/usr/bin/env python

from ConnectionManager import ConnectionManager
udpCon = ConnectionManager('udp')
udpCon.buildServer(9000)
udpCon.recv()

tcpCon = ConnectionManager('tcp')
tcpCon.buildServer(9001)
tcpCon.recv()
