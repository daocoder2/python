#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import socket


BUFF_SIZE = 1024  # 设置缓冲区大小
server_addr = ('127.0.0.1', 2333)  # IP和端口构成表示地址

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(server_addr)
print('waitting for data')
while True:
    data, client_addr = server.recvfrom(BUFF_SIZE)  # 从客户端接收数据
    print(bytes.decode(data))
    # 发送数据给客户端
    server.sendto(bytes(input('Please reply some string > '), 'utf8'), client_addr)
server.close()
