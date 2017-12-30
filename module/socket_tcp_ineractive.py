#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import socket
from threading import Thread


BUFF_SIZE = 1024  # 设置缓冲区大小
server_addr = ('127.0.0.1', 2333)  # IP和端口构成表示地址、端口必须数字


class ChatThread(Thread):
    def __init__(self, func):
        super(ChatThread, self).__init__()  # 调用父类的构造函数
        self.func = func  # 传入线程函数逻辑

    def run(self):
        self.func()


def re_data():
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


def se_data():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 返回新的socket对象
    except socket.error as e:
        print('Creating Socket Failure. Error Code : %d .Message : %s.' % (e.errno, e.strerror))
        sys.exit()
    client.connect(server_addr)  # 要连接的服务器地址
    while True:
        data = input('Please input some string > ')
        if not data:
            print('input can\'t empty, Please input again..')
            continue
        client.sendall(bytes(data, 'utf8'))  # 发送数据到服务器
        data = client.recv(BUFF_SIZE)  # 从服务器端接收数据
        print(bytes.decode(data))
    client.close()


def main():
    # 先创建线程对象
    t1 = ChatThread(re_data)
    t2 = ChatThread(se_data)
    # 启动所有线程
    t1.start()
    t2.start()
    # 等待动作
    t1.join()
    t2.join()


if __name__ == '__main__':
    main()
