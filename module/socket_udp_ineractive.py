#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import socket
from threading import Thread


BUFF_SIZE = 1024 # 设置缓冲区大小
server_addr = ('127.0.0.1', 2333) # IP和端口构成表示地址、端口必须数字

class ChatThread(Thread) :
    def __init__(self, func) :
        super(ChatThread, self).__init__()  # 调用父类的构造函数
        self.func = func  # 传入线程函数逻辑

    def run(self) :
        self.func()

def re_data() :
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(server_addr)
    print('waitting for data')
    while True:
        data, client_addr = server.recvfrom(BUFF_SIZE)  # 从客户端接收数据
        print(bytes.decode(data))
        # 发送数据给客户端
        server.sendto(bytes(input('Please reply some string > '), 'utf8'), client_addr)
    server.close()

def se_data() :
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 生成新的套接字对象
    while True:
        data = input('Please Input data > ')
        client.sendto(bytes(data, 'utf8'), server_addr)  # 向服务器发送数据
        data, addr = client.recvfrom(BUFF_SIZE)  # 从服务器接收数据
        print(bytes.decode(data))
    client.close()

def main() :
    # t1 = Thread(target = re_data)
    # t2 = Thread(target = se_data)
    # 先创建线程对象
    t1 = ChatThread(re_data)
    t2 = ChatThread(se_data)
    # 启动所有线程
    t1.start()
    t2.start()
    # 等待动作
    t1.join()
    t2.join()

if __name__ == '__main__' :
    main()