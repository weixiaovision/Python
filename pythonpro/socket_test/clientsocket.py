#!/usr/bin/python3
#-*- coding:utf-8 -*-


from socket import *


HOST = 'localhost'
PORT = 25678
BUFSIZE = 1024
ADDR = (HOST, PORT)

tcpclientsock = socket(AF_INET, SOCK_STREAM)
tcpclientsock.connect(ADDR)

while True:
    data = input('> ')
    if not data:
        break
    tcpclientsock.send(bytes(data, 'utf-8'))
    data = tcpclientsock.recv(BUFSIZE)
    if not data:
        break
    print(data.decode('utf-8'))

tcpclientsock.close()
