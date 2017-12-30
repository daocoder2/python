
# python模块（包）之socket

[socket：官方文档是最好的模块表达说明。](https://docs.python.org/3.6/library/socket.html)

## socket

## 1、socket基础

### 1.1 socket基本概念

网络上两个程序通过一个双向的通信连接实现数据的交换，这个连接的一端称为socket。

网络通信，归根结底还是计算机之间进程之间的通信。在网络中，每一个计算机看作一个节点，它们都有一个网络地址，也就是ip地址，仅根据ip地址只能确定计算机的位置，而一台计算机可能运行多个不同的进程（程序），所以套接字还需要一个端口号来确定某一进程。即ip地址+进程端口号=唯一进程，暂理解为一个socket。

建立网络通信至少要一对套接字（socket），它通常用于描述ip地址和端口，是一个通信链的句柄，可以用来实现不同的虚拟机或不同计算机之间的通信。

每一个socket都用一个半相关描述（协议、地址和本机端口）来表示；一个完整的套接字则用一个相关描述（协议、本地地址、本地端口、远程地址和远程端口）。socket也有一个类似于打开文件的函数调用，该函数返回一个整型的socket描述符，随后的连接建立、数据传输等操作都是通过socket来实现。

### 1.2 socket深入理解

[简单的网络通信介绍。](http://blog.csdn.net/prl18353364833/article/details/51593643)

HTTP协议对应于应用层，TCP协议对应于传输层，IP协议对应于网络层，HTTP协议是基于TCP连接的,三者本质上没有可比性。TCP/IP是传输层协议，主要解决数据如何在网络中传输；而HTTP是应用层协议，主要解决如何包装数据。**socket是应用层与TCP/IP协议族通信的中间软件抽象层，是它的一组接口。**

**socket.socket(family=AF_INET, type=SOCK_STREAM, proto=0, fileno=None)**：初始化创建一个socket对象。

1、family参数指定哪个协议用在当前套接字上。

- AF_INET：IPv4 网络协议。TCP 和 UDP 都可使用此协议。 
- AF_INET6：IPv6 网络协议。TCP 和 UDP 都可使用此协议。 
- AF_UNIX：本地通讯协议。具有高性能和低成本的IPC（进程间通讯）。

2、type参数指常用的socket类型有3种：

- 流式socket（SOCK_STREAM）：提供一个顺序化的、可靠的、全双工的、基于连接的字节流。支持数据传送流量控制机制。TCP协议即基于这种流式套接字。
- 数据报socket（SOCK_DGRAM）：提供数据报文的支持。(无连接，不可靠、固定最大长度)。UDP协议即基于这种数据报文套接字。
- 原生socket（SOCK_RAW）：提供读取原始的网络协议。这种特殊的套接字可用于手工构建任意类型的协议。一般使用这个套接字来实现ICMP请求（例如 ping）。 

## 2、socket通信连接过程

根据连接启动的方式以及本地套接字要连接的目标，套接字之间的连接过程可以分为三个步骤：服务器监听，客户端请求，连接确认。

**1、服务器监听**：是服务器端套接字并不定位具体的客户端套接字，而是处于等待连接的状态，实时监控网络状态。

即：服务器端运行一个进程（创建socket对象），绑定一个端口，再后台运行处于监听状态，等待请求来建立通信连接。

**2、客户端请求**：是指由客户端的套接字提出连接请求，要连接的目标是服务器端的套接字。为此，客户端的套接字必须首先描述它要连接的服务器的套接字，指出服务器端套接字的地址和端口号，然后就向服务器端套接字提出连接请求。

即：客户端运行一个进程（创建socket对象），指明服务器端的地址和端口，向服务器端套接字发出通信连接请求。

**3、连接确认后通信**：是指当服务器端套接字监听到或者说接收到客户端套接字的连接请求，它就响应客户端套接字的请求，建立一个新的线程，把服务器端套接字的描述发给客户端，一旦客户端确认了此描述，连接就建立好了。而服务器端套接字继续处于监听状态，继续接收其他客户端套接字的连接请求。

## 3、python模拟socket通信

### 3.1 基于tcp通信

![SOCK_STREAM通信示意图](https://i.imgur.com/RVHY1LY.png)

**1、服务器端函数**

**以下默认socket为socket.socket()创建的socket对象。**

**socket.bind(address)**：socket对象绑定监听地址和端口。

- address为一个元组(host, port)。host为ip地址，port为端口。

**socket.listen([backlog])**：进程处于监听状态，等待网络中某一客户机的连接请求。

- backlog操作系统可以挂起的最大连接数量，该值至少为1，大部分程序设为5就可以。

**socket.accept()**：接受远程计算机的连接请求，建立起与客户机之间的通信连接。服务器处于监听状态时，如果某时刻获得客户机的连接请求，此时并不是立即处理这个请求，而是将这个请求放在等待队列中，当系统空闲时再处理客户机的连接请求。

- 返回元组(conn, address)，其中conn是新的套接字对象，可以用来接收和发送数据。address是客户端连接的地址。

**2、客户端函数**

**socket.connect(address)**：连接远程服务器。

- address为一个元组(host, port)。host为ip地址，port为端口。如果连接出错，返回socket.error错误。

**3、通用函数**

**socket.recv(bufsize[, flags])**：接收远程主机发送的数据。

- bufsize为指定要接收数据的大小。
- flags提供有关消息的其它信息，通常可以忽略。
- 返回值为字符串形式的数据。

**socket.send(bytes[, flags])**：发送数据给指定主机。

- bytes为要发送的字符串数据。
- flags提供有关消息的其它信息，通常可以忽略。
- 返回值为要发送的字节数量，该数量可能小于bytes的字节大小。

**socket.sendall(bytes[, flags])**：完整发送TCP数据。将string中的数据发送到连接的套接字，但在返回之前会尝试发送所有数据。

- 返回值 : 成功返回None，失败则抛出异常。

**socket.close()**：关闭socket对象。

### 3.2 socket_tcp代码

**1、服务器端**

	#!/usr/bin/python
	# -*- coding:utf-8 -*-
	
	import sys
	import socket
	
	
	BUFF_SIZE = 1024 # 设置缓冲区大小
	server_addr = ('127.0.0.1', 2333) # IP和端口构成表示地址
	
	try :
	    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
	except socket.error as e:
	    print('Creating Socket Failure. Error Code : %d .Message : %s.' %(e.errno, e.strerror))
	    sys.exit()
	try :
	    server.bind(server_addr)
	except socket.error as e :
	    print('Socket Binding Failure. Error Code : %d .Message : %s.' %(e.errno, e.strerror))
	    sys.exit()
	server.listen(5) # 最大监听数为5
	while True :
	    client_socket, client_addr = server.accept()  # 接收TCP连接, 并返回新的套接字和地址, 阻塞函数
	    print('Connected by ', print(client_addr))
	    while True :
	        data = client_socket.recv(BUFF_SIZE)  # 从客户端接收数据
	        print(bytes.decode(data))
	        client_socket.sendall(bytes(input('Please reply some string > '), 'utf8'))
	server.close()

**2、客户端**

	#!/usr/bin/python
	# -*- coding:utf-8 -*-
	
	import sys
	import socket
	
	
	BUFF_SIZE = 1024  # 设置缓冲区的大小
	server_addr = ('127.0.0.1', 2333) # IP和端口构成表示地址
	try :
	    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 返回新的socket对象
	except socket.error as e :
	    print('Creating Socket Failure. Error Code : %d .Message : %s.' %(e.errno, e.strerror))
	    sys.exit()
	client.connect(server_addr)  # 要连接的服务器地址
	while True:
	    data = input("Please input some string > ")
	    if not data :
	        print('input can\'t empty, Please input again..')
	        continue
	    client.sendall(bytes(data, 'utf8'))  # 发送数据到服务器
	    data = client.recv(BUFF_SIZE)  # 从服务器端接收数据
	    print(bytes.decode(data))
	client.close()

**3、简单交互演示**

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
	
	def se_data() :
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

### 3.3 基于udp通信

![SOCK_DGRAM通信示意图](https://i.imgur.com/1jDrcfb.png)

**1、通用函数**

**以下默认socket为socket.socket()创建的socket对象。**

**socket.sendto(bytes [,flag], address)**：发送udp数据，将数据发送到套接字。

- bytes，二进制字节序列形式发送数据。
- address，远程地址，(host, port)元组。
- 返回值，发送的字节数。

**socket.recvfrom(bufsize[, flags])**：接收udp套接字的数据，与上面recv()功能相似。

- bufsize，指定要接收的数据大小。
- 返回值，(data,address)元组, 其中data是包含接收数据的字符串，address是发送数据的套接字地址。
- flag : 提供有关消息的其他信息，通常可以忽略。

### 3.4 socket_udp代码

**1、服务器端**

	#!/usr/bin/python
	# -*- coding:utf-8 -*-
	
	import sys
	import socket
	
	
	BUFF_SIZE = 1024 # 设置缓冲区大小
	server_addr = ('127.0.0.1', 2333) # IP和端口构成表示地址
	
	server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	server.bind(server_addr)
	print('waitting for data')
	while True :
	    data, client_addr = server.recvfrom(BUFF_SIZE)  # 从客户端接收数据
	    print(bytes.decode(data))
	    # 发送数据给客户端
	    server.sendto(bytes(input('Please reply some string > '), 'utf8'), client_addr)
	server.close()

**2、客户端**

	#!/usr/bin/python
	# -*- coding:utf-8 -*-
	
	import sys
	import socket
	
	
	BUFF_SIZE = 1024  # 设置缓冲区的大小
	server_addr = ('127.0.0.1', 2333) # IP和端口构成表示地址
	
	client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 生成新的套接字对象
	while True :
	    data = input('Please Input data > ')
	    client.sendto(bytes(data, 'utf8'), server_addr)  # 向服务器发送数据
	    data, addr = client.recvfrom(BUFF_SIZE)  # 从服务器接收数据
	    print(bytes.decode(data))
	client.close()

**3、简单交互演示**

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

## 4、后面的坑

1、端口必须是整数

2、bytes和str的相互转换。

Bytes对象是由单个字节作为基本元素（8位，取值范围0-255）组成的序列，为不可变对象。

Bytes 对象只负责以二进制字节序列的形式记录所需记录的对象，至于该对象到底表示什么（比如到底是什么字符）则由相应的编码格式解码所决定。

[python 标准数据类型：Bytes](https://segmentfault.com/a/1190000004450876)

[Python 3.x Error：TypeError: a bytes-like object is required, not 'str'](http://blog.csdn.net/bible_reader/article/details/53047550)
