#!/usr/bin/python3
#-*- coding:utf-8 -*-


from socket import *
from time import ctime


HOST = 'localhost'
PORT = 25678
BUFSIZE = 1024
ADDR = (HOST, PORT)

TCPsERSOCK = socket(AF_INET, SOCK_STREAM)
TCPsERSOCK.bind(ADDR)
TCPsERSOCK.listen(5)


while True:
    print('waiting for connection')
    tcpClientSock, addr = TCPsERSOCK.accept()
    print('connected from :', addr)

    while True:
        data = tcpClientSock.recv(BUFSIZE)
        print(data.decode('utf-8'))
        if not data:
            break
        tcpClientSock.send('[%s] %s' % (bytes(ctime(), 'utf-8'), data))

    tcpClientSock.close()

TCPsERSOCK.close()
