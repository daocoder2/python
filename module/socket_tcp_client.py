#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import socket


BUFF_SIZE = 1024  # 设置缓冲区的大小
server_addr = ('127.0.0.1', 2333) # IP和端口构成表示地址
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 返回新的socket对象
except socket.error as e:
    print('Creating Socket Failure. Error Code : %d .Message : %s.' %(e.errno, e.strerror))
    sys.exit()
client.connect(server_addr)  # 要连接的服务器地址
while True:
    data = input("Please input some string > ")
    if not data:
        print('input can\'t empty, Please input again..')
        continue
    client.sendall(bytes(data, 'utf8'))  # 发送数据到服务器
    data = client.recv(BUFF_SIZE)  # 从服务器端接收数据
    print(bytes.decode(data))
client.close()
