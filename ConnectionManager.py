#!/usr/bin/env python
import select
import socket
class ConnectionManager(object):


    def __init__(self, connType):
        '''
            connType -- string is eiter tcp or udp
        '''
        self.connType = connType
        self.clientsock = []


    def buildServer(self, port):
        '''
        builds the server for the particular connection type
        '''
        if self.connType == 'tcp':
            self.server_socket, self.addr = self.tcpConnection('', port)
        else:
            ## else we are udp
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.server_socket.bind(('', port))

    def tcpConnection(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(1)
        return sock.accept()

    def addClient(self, ip, port):
        self.isServer = False
        if self.connType == 'tcp':
            self.clientsock.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
            self.clientsock[len(self.clientsock) -1].connect((ip, port))
        else:
            ## else we are udp
            self.clientsock.append((ip, port, socket.socket(socket.AF_INET, socket.SOCK_DGRAM)))

    def send(self, data):
        '''
            Will send data to the client if you are a tcp server
            Will NOT send data if you are a UDP server
            Will send data to all of the client connections if a client
            Will send data to all udp servers if you are a udp client
        '''
        if self.isServer == True and self.connType == 'tcp':
            self.server_socket.sendall(data)
        elif self.isServer == True and self.connType == 'udp':
            ## THIS IS NOT POSSIBLE IF YOU ARE A UDP SERVER you can't send
            ## make it a client then you can send.
            return False
        elif self.isServer == False and self.connType == 'tcp':
            _,ready_socks,_ = select.select([], self.clientsock, [])
            for sock in ready_socks:
                sock.sendall(data) # This is will not block
                print "sent message:", data
        elif self.isServer == False and self.connType == 'udp':
            for sockinfo in self.clientsock:
                print 'Sending %s to %s :%d' %(data, sockinfo[0], sockinfo[1])
                sockinfo[2].sendto(data, (sockinfo[0], sockinfo[1]))
        return True

    def recv(self):
        '''
        Actually the same for both server and client
        returns a dict where the key is the ('ip', port)
        may be empty if nothing
        '''
        recvData = {}
        ready_socks,_,_ = select.select([self.server_socket], [], [])
        for sock in ready_socks:
            data, addr = sock.recvfrom(4096) # This is will not block
            recvData[addr] = data
            print "received message:", data
        return recvData
