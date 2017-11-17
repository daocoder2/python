#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import socket


BUFF_SIZE = 1024  # 设置缓冲区的大小
server_addr = ('127.0.0.1', 2333)  # IP和端口构成表示地址

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 生成新的套接字对象
while True:
    data = input('Please Input data > ')
    client.sendto(bytes(data, 'utf8'), server_addr)  # 向服务器发送数据
    data, addr = client.recvfrom(BUFF_SIZE)  # 从服务器接收数据
    print(bytes.decode(data))
client.close()
