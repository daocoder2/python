#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import socket


BUFF_SIZE = 1024  # 设置缓冲区大小
server_addr = ('127.0.0.1', 2333)  # IP和端口构成表示地址

try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
except socket.error as e:
    print('Creating Socket Failure. Error Code : %d .Message : %s.' % (e.errno, e.strerror))
    sys.exit()
try:
    server.bind(server_addr)
except socket.error as e:
    print('Socket Binding Failure. Error Code : %d .Message : %s.' % (e.errno, e.strerror))
    sys.exit()
server.listen(5)  # 最大监听数为5
while True:
    client_socket, client_addr = server.accept()  # 接收TCP连接, 并返回新的套接字和地址, 阻塞函数
    print('Connected by ', print(client_addr))
    while True:
        data = client_socket.recv(BUFF_SIZE)  # 从客户端接收数据
        print(bytes.decode(data))
        client_socket.sendall(bytes(input('Please reply some string > '), 'utf8'))
server.close()
