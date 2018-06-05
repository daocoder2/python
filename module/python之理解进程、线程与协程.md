<div class="BlogAnchor">
   <p>
   <b id="AnchorContentToggle" title="收起" style="cursor:pointer;">目录[+]</b>
   </p>
  <div class="AnchorContent" id="AnchorContent"> </div>
</div>

# python之进程、线程与协程

有这么个例子说他们的区别，帮助理解很有用。

- 有一个老板想开一个工厂生产手机。
- 他需要花一些财力、物力及人力去制作一条生产线，这条线上所有的钱、人、物料准备：为了生产手机的储备资源称之为**进程**。
- 有了生产线，老板负责把资源统一管理调度起来，然后还需要一个工人按照生产手机的工艺、去按部就班地把手机做出来。这个做事情的工人就叫**线程**。
- 然后生产线可以运作起来了，但是效率低，手机供不应求。为了提高生产效率，老板又想了几个办法；
	-  在这条生产线上多招几个工人，一起来做手机，这样效率就增加了。即**单进程、多线程模式**。
	-  之后老板又发现，单条生产线的工人并不是越多越好，因为一条生产线的资源、空间等有限，所以老板又花了财力物力去置办了另外一条生产线，然后在招一些工人，效率又上去了。即**多进程、多线程模式**。
	-  现在已经有个多条生产线和多个工人（多进程、每个进程对应多条线程）。但是老板发现，有时工人按照生产手机的工艺工作时，有时是为了等待上一道工序的完成是闲下来的，就侃大山去了。资本家么，就想了一个办法：如果某个员工在工作时临时没事或者在等待另一个工人生产完谋道工序之后他才能再次工作，那么这个员工就利用这个时间去做其它的事情。那么也就是说：如果一个线程等待某些条件，可以充分利用这个时间去做其它事情。即**协程**。

这里再总结术语有下面几点：

- 进程是资源分配和调度资源的最小单位。
- 线程是进程的实体，是系统分配和调度的基本单位。
- 进程切换需要的资源很最大，效率很低。
- 线程切换需要的资源一般，效率一般（当然了在不考虑GIL的情况下）。
- 协程切换任务资源很小，效率高。
- 多进程、多线程根据cpu核数不一样可能是并行的，但是协程是在一个线程中，所以是并发。

# 1、多任务的需求

在演唱会中，很多歌手都是歌舞一起表演，那加入用程序来模拟的话，就大概是这样。

	from time import sleep
	
	
	def sing():
	    for i in range(3):
	        print('我在唱歌')
	        sleep(1)
	
	
	def dance():
	    for i in range(3):
	        print('我在跳舞')
	        sleep(1)
	
	
	if __name__ == '__main__':
	    sing()
	    dance()

结果：

	我在唱歌
	我在唱歌
	我在唱歌
	我在跳舞
	我在跳舞
	我在跳舞

上面运行的程序并没有完成唱歌和跳舞同时进行的要求，那如果想要实现“唱歌跳舞”同时进行，那么就需要一个新的方方法：多任务。

那什么叫多任务。简而言之就是系统可以同时运行多个任务。比如你聊天的时候可以听歌，还可以浏览网页等。

要实现它有很多方式，以前是单核cpu，由于cpu执行代码都是顺序执行的，那么单核cpu就轮流让各个任务交替执行，这样反复执行下去。表面上看，每个任务都是交替执行的，但是，由于cpu的执行速度比较快，我们感觉就像所有任务都在同时执行一样。

真正的**并行**执行多任务只能在多核cpu上实现，但是由于任务数量远远多于cpu的核心数量，所以系统也会自动把很多任务轮流调度到每个核心上执行。

这里涉及到两个概念。

- **并发**：任务数多于cpu核数，通过操作系统的各种任务调度算法，实现用多个任务“一起”执行（实际上一些任务不在执行，因为切换任务的速度相当快，看上去一起执行而已）。
- **并行**：任务数小于等于cpu核数，即任务真的是一起执行的。

# 2、线程

python的thread模块是比较底层的模块，python的threading模块是对thread做了一些封装，可以更加方便的被使用。

## 2.1 使用threading模块

**1、单线程执行一个任务**

	from time import sleep
	
	
	def study_apologise():
	    print('钢铁直男是要学会道歉的。')
	    sleep(1)
	
	
	if __name__ == '__main__':
	    for i in range(5):
	        study_apologise()

结果就不少于5s学习时间。

**2、多线程执行一个任务**

	import threading
	from time import sleep
	
	
	def study_apologise():
	    print('钢铁直男是要学会道歉的。')
	    sleep(1)
	
	
	if __name__ == '__main__':
	    for i in range(5):
	        muti_threaing = threading.Thread(target=study_apologise)
	        muti_threaing.start()

结果就秒出了，可以明显看出使用了多线程并发的操作，花费时间要短很多。且当调用start()时，才会真正的创建线程，并且开始执行。

**3、主线程会等待所有的子线程结束后才结束**

	from time import sleep
	import threading
	
	
	def sing():
	    for i in range(3):
	        print('我在唱歌')
	        sleep(1)
	
	
	def dance():
	    for i in range(3):
	        print('我在跳舞')
	        sleep(1)
	
	
	if __name__ == '__main__':
	    my_sing = threading.Thread(target=sing)
	    my_dance = threading.Thread(target=dance)
	    my_sing.start()
	    my_dance.start()
	    # sleep(5)
	    print('---结束---')

这里主进程会一直向下进行，子进程代码继续运行，当所有子进程结束后，主进程才会结束。

**4、查看线程数量**

	from time import sleep
	import threading
	
	
	def sing():
	    for i in range(3):
	        print('我在唱歌')
	        sleep(1)
	
	
	def dance():
	    for i in range(3):
	        print('我在跳舞')
	        sleep(1)
	
	
	if __name__ == '__main__':
	    my_sing = threading.Thread(target=sing)
	    my_dance = threading.Thread(target=dance)
	    my_sing.start()
	    my_dance.start()
	    # sleep(5)
	    while True:
	        thread_count = len(threading.enumerate())
	        print('当前的进程数为 %d' % thread_count)
	        if thread_count <= 1:
	            break
	        sleep(0.5)

结果为：

	我在唱歌 0
	我在跳舞 0
	当前的进程数为 3
	当前的进程数为 3
	当前的进程数为 3
	我在跳舞 1
	我在唱歌 1
	当前的进程数为 3
	我在唱歌 2
	我在跳舞 2
	当前的进程数为 3
	当前的进程数为 3
	当前的进程数为 2
	当前的进程数为 1

## 2.2 线程执行代码的封装

在上面可以体现出，通过threading模块能完成多任务的程序开发。为了让每个线程封装的更完美，在实际使用threading模块时，通常会定义一个新的子类，这个子类继承threading.Thread，然后重写它的run方法，上面的这个例子就可以写成下面这样。

	from time import sleep
	import threading
	
	
	class Sing(threading.Thread):
	    def run(self):
	        for i in range(3):
	            print('我在唱歌 %d' % i)
	            sleep(1)
	
	
	class Dance(threading.Thread):
	    def run(self):
	        for i in range(3):
	            print('我在跳舞 %d' % i)
	            sleep(1)
	
	
	if __name__ == '__main__':
	    my_sing = Sing()
	    my_dance = Dance()
	    my_sing.start()
	    my_dance.start()
	    # sleep(5)
	    while True:
	        thread_count = len(threading.enumerate())
	        print('当前的进程数为 %d' % thread_count)
	        if thread_count <= 1:
	            break
	        sleep(0.5)

结果是一样的。

再一个小demo。

	from time import sleep
	import threading
	
	
	class MyThread(threading.Thread):
	    def run(self):
	        for i in range(3):
	            # name属性中保存的是当前线程的名字
	            print("this is %d thread and it's name is %s" % (i, self.name))
	            sleep(1)
	
	
	if __name__ == '__main__':
	    my_thread = MyThread()
	    my_thread.start()

threading.Tread类中有一个run方法，用于定义线程的功能函数，可以在自己的线程类中覆盖该方法。创建自己的线程实例对象后，可以通过Tread的start方法，可以启动该线程。当线程获得执行的机会时，就会调用run方法。

- 每个线程都有一个名字，尽管上面的例子中没有指定线程对象的name，但python会自动为线程指定一个名字。
- 当线程的run方法完成时，该线程完成。
- 程序无法控制线程的调度顺序，但可以通过别的方式去影响线程调度的方式。

## 2.3 线程：全局作用变量共享

	from time import sleep
	import threading
	
	my_num = 10
	
	
	class MyThreadOne(threading.Thread):
	    def run(self):
	        global my_num
	        for i in range(5):
	            my_num += 1
	        print('线程1执行后 %d' % my_num)
	
	
	class MyThreadTwo(threading.Thread):
	    def run(self):
	        global my_num
	        print('线程2执行后 %d' % my_num)
	
	
	if __name__ == '__main__':
	    print('多线程执行前 %d' % my_num)
	    my_thread_one = MyThreadOne()
	    my_thread_one.start()
	    sleep(2)
	    my_thread_two = MyThreadTwo()
	    my_thread_two.start()

结果如下，很明显地看出线程之间是共享全局变量的。

	多线程执行前 10
	thread_one, my_num is 15---
	线程1执行后 15
	thread_two, my_num is 15---
	线程2执行后 15

当列表当作实参传递到线程中。

	from time import sleep
	import threading
	
	my_num = [11, 22, 33]
	
	
	class MyThreadOne(threading.Thread):
	    def __init__(self, args=()):
	        self.num = args[0]
	        super(MyThreadOne, self).__init__()
	
	    def run(self):
	        self.num.append(44)
	    	print('线程1执行后 ', my_num)
	
	
	class MyThreadTwo(threading.Thread):
	    def run(self):
	        print('线程2执行后', my_num)
			pass
			
	
	
	if __name__ == '__main__':
	    print('多线程执行前 ', my_num)
	    my_thread_one = MyThreadOne(args=(my_num,))
	    my_thread_one.start()
	    sleep(2)
	    my_thread_two = MyThreadTwo(args=(my_num,))
	    my_thread_two.start()

- 在一个进程内所有线程共享全局变量，很方便在多个进程间进行共享数据。
- 优劣并存的是线程对全局变量的随意修改可能会造成多线程之间对全局变量的混乱。

共享造成的混乱，还是上面类似的代码：

	from time import sleep
	import threading
	
	my_num = 100000
	
	
	class MyThreadOne(threading.Thread):
	    def run(self):
	        global my_num
	        for i in range(100000):
	            my_num += 1
			print('线程1执行后 %d' % my_num)
	
	
	class MyThreadTwo(threading.Thread):
	    def run(self):
	        global my_num
	        for i in range(100000):
	            my_num += 1
			  print('线程2执行后 %d' % my_num)
	
	
	if __name__ == '__main__':
	    print('多线程执行前 %d' % my_num)
	    my_thread_one = MyThreadOne()
	    my_thread_one.start()
	    sleep(2)
	    my_thread_two = MyThreadTwo()
	    my_thread_two.start()
	  

结果这样：

	多线程执行前 100000
	线程1执行后 159679
	线程2执行后 259832

每次运行不一样，原因如下：

1、在my_num=0时，线程1取得my_num=0。此时系统把线程1调度为‘sleeping’状态，把线程2转换为‘running’状态，t2也获得my_num=0。
2、线程2对得到的值进行加1并赋给my_num，使得my_num=1。
3、系统又把线程2调度为‘sleeping’，把线程1转为‘running’。线程线程1又把它之前得到的0加1后赋值给my_num。
4、这样导致线程1和2都对my_num加1，但结果仍然是my_num=1。

**重点：如果多个线程同时对同一个全局变量进行操作，会出现资源竞争问题，从而导致运算结果会不正确。**

## 2.4 同步与互斥锁

同步不是说一起同时，而是协同配合。比如上面的问题，线程1、2在操作my_num时，发现对方在用，就延迟一会再用，相互等待，两个同时只执行1个就可以做到同步。

**线程同步同步**的实现用到**互斥锁**。

当多个线程同时修改某一个共享数据时，就要进行同步控制。最简单的机制就是互斥锁。**互斥锁为资源的引入状态：锁定/非锁定。**

某个线程需要修改一个共享数据时，先将这个数据进行“锁定”，然后对其做修改。这个共享数据被锁定时，其它线程不能修改，知道该数据的状态变成“非锁定”，其它线程才能再次锁定该资源。互斥锁保证每个只有一个线程进行写入操作，从而保证了多线程情况下数据的准确性。

threading.Lock封装了互斥锁，可以方便的对其进行操作。方法如下：

	mutex = threading.Lock()
	mutex.acquire()
	mutex.release()

- 如果这个资源之前是没上锁的，那么acquire()不会堵塞。
- 如果调用acquire()对这个资源进行上锁之前，它已经被其它线程上了锁，那么此时acquire()会堵塞，直到这个锁被释放为止。

按这样的步骤再运行上面数据运算失败的例子，如下，最后得到正确的结果。

	多线程执行前 100000
	线程1执行后 258195
	线程2执行后 300000

上锁解锁的过程：当一个线程调用锁的acquire()方法获得锁，锁就进入“locked”的状态。每次只有一个线程可以获得锁。如果另一个线程试图获得这个锁，该线程会变为“blocked”，成为堵塞，直到拥有锁的线程的release()方法释放锁后，锁进入“unlock”状态。线程调度程序从出于堵塞状态中的线程选择一个获得锁，并使得该线程进入到运行“running”状态。

特点：

- 某段关键代码只能由一个线程从头到尾地完整执行。
- 阻止了多线程的并发执行，包含锁的某段代码实际上就只能单线程模式执行，效率降低。
- **由于可以存在多个锁，不同的线程持有不同的锁，并试图获取对方持有的锁时，可能会造成死锁。**

## 2.5 死锁

在线程间共享多个资源的时候，如果两个线程分别占有一部分资源并等待对方的资源，这样就会造成死锁。尽管死锁很少发送，但一旦发生就会造成应用停止响应。

	from time import sleep
	import threading
	
	my_num = 100000
	mutex_a = threading.Lock()
	mutex_b = threading.Lock()
	
	
	def thread_a():
	    mutex_a.acquire()
	    print('获取到了a锁，2s后尝试获取b锁')
	    sleep(2)
	    mutex_b.acquire()
	    print('已获取b锁')
	    mutex_b.release()
	    mutex_a.release()
	
	
	def thread_b():
	    mutex_b.acquire()
	    print('获取到了b锁，2s后尝试获取a锁')
	    sleep(2)
	    mutex_a.acquire()
	    print('已获取a锁')
	    mutex_a.release()
	    mutex_b.release()
	
	
	if __name__ == '__main__':
	    print('死锁模拟')
	    a = threading.Thread(target=thread_a)
	    a.start()
	    b = threading.Thread(target=thread_b)
	    b.start()

运行结果如下：

	死锁模拟
	获取到了a锁，2s后尝试获取b锁
	获取到了b锁，2s后尝试获取a锁

这样一来，就要考虑如何避免死锁，通常两种方案。

- 程序设计尽量避免（银行家算法、生产者与消费者）
- 添加超时时间，释放锁

## 2.6 Condition与生产者与消费者问题

python提供的threading.Condition对象提供了对复杂线程同步支持的问题。

Condition被称为条件变量，除了提供与Lock类似的acquire、release方法之外，还提供了wait和notify方法。

使用情景：线程首先acquire获取条件变量，然后再进行一些条件判断，如果条件满足，则进行一些处理改变条件后再通过notify方法通知其它线程，其它出于wait状态的线程接到条件后会重新进行条件判断。若条件不满足则wait，等待notify通知。如此不断反复这一过程。

那经典的生产者与消费者的问题描述的是：假设一群生产者（Producer）和一群消费者（Consumer）通过一个市场来交换东西。生产者的策略是如果市场的剩余产品少于5个，那么就生产一个产品放到市场上。而消费者的策略是如果市场上剩余的产品多于5个，就消费1个产品。

	from time import sleep
	import threading
	import random
	
	MAX_SIZE = 5
	SHARE_Q = []
	
	
	class Producer(threading.Thread):
	    def run(self):
	        products = range(MAX_SIZE)
	        global SHARE_Q
	        while True:
	            condition.acquire()
	            if len(SHARE_Q) == MAX_SIZE:
	                print('Market is full')
	                condition.wait()
	                print('Consumer must do shmething')
	            else:
	                product = random.choice(products)
	                SHARE_Q.append(product)
	                print("Producer: ", product)
	                condition.notify()
	            condition.release()
	            sleep(random.random())
	
	
	class Consumer(threading.Thread):
	    def run(self):
	        global SHARE_Q
	        while True:
	            condition.acquire()
	            if not SHARE_Q:
	                print('Market is empty')
	                condition.wait()
	                print('Producer must do shmething')
	            else:
	                product = SHARE_Q.pop()
	                print("Consumer: ", product)
	                condition.notify()
	            condition.release()
	            sleep(random.random())
	
	
	if __name__ == '__main__':
	    print('生产者与消费者')
	    condition = threading.Condition()
	    a = Producer()
	    a.start()
	    b = Consumer()
	    b.start()

# 2、进程

## 2.1 进程及进程的状态

**1、进程**

程序：这是一个py跑的程序，指一个静态的概念。

进程：一个程序运行起来之后，运行的代码和用到的资源称之为进程，它是操作系统分配资源的基本单位。

**2、进程的状态**

一般的计算机运行情况是任务数大于cpu数，即一些任务正在运行，另一些任务在等待cpu执行的情况，因此导致了任务有不同的状态。

- 就绪态：运行的条件都已经满足，正在等在cpu执行。
- 执行态：cpu正在执行其功能。
- 等待态：等待某些条件满足，例如一个程序sleep了，此时就处于等待态。

## 2.2 进程的创建与使用

multiprocessing模块是跨平台版本的多进程模块，提供了一个Process类来代表一个进程对象，这个对象可以理解为一个独立的进程，可以执行另外的事情。

**1、简单进程跑起来**

	from multiprocessing import Process
	from time import sleep,ctime
	
	
	def my_process():
	    while True:
	        print('----new process')
	        sleep(1)
	
	
	if __name__ == '__main__':
	    new_process = Process(target=my_process)
	    new_process.start()
	    while True:
	        print('----running process')
	        sleep(1)

结果：

	----running process
	----new process
	----running process
	----new process
	----running process
	----new process
	----running process

- 创建子进程时，只需要传入一个可执行函数和对应参数，创建一个Process()实例，用start()方法就可以了。

**2、函数传参及进程id**

	from multiprocessing import Process
	from time import sleep,ctime
	import os
	
	
	def my_process(pm, *args, **kwargs):
	    print('----son process id is %s and parent is is %s' % (os.getpid(), os.getppid()))
	    print(pm)
	    for i, v in enumerate(args):
	        print(i, v)
	    for key, value in kwargs.items():
	        print(key, value)
	    sleep(1)
	
	
	if __name__ == '__main__':
	    new_process = Process(target=my_process, args=('first', 'second'), kwargs={'test': 'first'})
	    new_process.start()
	    print('----parent process id is %s ' % os.getpid())
	    sleep(1)

结果：

	----parent process id is 4292 
	----son process id is 8656 and parent is is 4292
	0 first
	1 second
	test first

可以看出，创建出来的进程是当前运行进程的子进程。

**3、Process详解**

Process的语法结构：

	Process([group [, target [, name [, args [, kwargs]]]]])

- target：如果函数传递了函数的引用，可以认为创建的子进程就执行它的代码。
- args：给target传递参数，以元组的形式传入。
- kwargs：给target指定的函数传递命名参数，字典形式。
- name：给程序设定一个名字，也可以不设定。
- group：指定进程组，大部分情况下用不到。

Process的创建的实例对象的常用方法：

- start()：启动子进程实例（创建子进程）。
- is_alive()：判断子进程是否存活。
- join()：是否等待子进程执行结束或等待多少秒。
- terminate()：不管任务是否完成，强制终止子进程。

Process()创建实例对象的常用属性：

name：当前进程的别名，默认为Process-N，N为从1开始递增的整数。
pid：当前进程的pid。

**4、进程之间不共享全局变量**

	from multiprocessing import Process
	from time import sleep,ctime
	import os
	
	global_list = [1, 2, 3, 4, 5]
	
	
	def process_one(param):
	    print('process_one pid=%s ' % os.getpid())
	    param.append(6)
	    print(param)
	
	
	def process_two(param):
	    print('process_two pid=%s ' % os.getpid())
	    print(param)
	
	
	if __name__ == '__main__':
	    process_ob_one = Process(target=process_one, args=(global_list, ))
	    process_ob_one.start()
	    print(process_ob_one.name)
	    sleep(2)
	    proces_ob_two = Process(target=process_two, args=(global_list, ))
	    proces_ob_two.start()
	    print(proces_ob_two.name)

结果：

	Process-1
	process_one pid=8984 
	[1, 2, 3, 4, 5, 6]
	Process-2
	process_two pid=9200 
	[1, 2, 3, 4, 5]

- 每个实例对象的name从1依次递增。
- 全局变量不共享。

## 2.3 进程与线程的区别

进程是系统进行资源分配和调度的独立单位。线程是一个实体，是cpu调度和分配的基本单位，它是比进程更小的能独立运行的基本单位。线程自己基本上不拥有系统资源，只拥有一点在运行中必不可少的资源（如程序计算器、一组寄存器和栈），但是它可以共享**同属一个进程的其它线程**共享进程所拥有的全部资源。

同时总结有以下几个特点。

- 一个程序至少有一个进程，一个进程至少有一个线程，线程不能独立执行，必须依存在进程中。
- 线程的划分尺度小于进程（资源比进程少），使得多线程的并发性高。
- 进程在执行过程中拥有独立的内存单元，而多个线程共享内存，从而极大地提高了程序的运行效率。
- 线程的执行开销小，不利于系统资源的管理和保护，进程相反。

## 2.4 进程之间的通信

Process之间有时需要通信，操作系统提供了很多机制来实现进程之间的通信。

**1、Queen的使用**

可以用multiprocessing模块的Queen实现进程之间的数据传递，Queen本身是一个消息队列程序。

	from multiprocessing import Queue
	
	
	msg_queen = Queue(3)
	msg_queen.put('first msg')
	msg_queen.put('second msg')
	msg_queen.put('third msg')
	print(msg_queen.full())
	try:
	    msg_queen.put('fourth msg', True, 3)
	except:
	    print('msg is full, its size is %d' % msg_queen.qsize())
	
	try:
	    msg_queen.put_nowait('fourth msg')
	except:
	    print('msg is full, without timeout, its size is %d' % msg_queen.qsize())
	
	if not msg_queen.full():
	    msg_queen.put_nowait('先判断再写入消息')
	if not msg_queen.empty():
	    for i in range(msg_queen.qsize()):
	        # 先判断再获取
	        print(msg_queen.get_nowait())

结果：

	True
	msg is full, its size is 3
	msg is full, without timeout, its size is 3
	first msg
	second msg
	third msg

**2、Queen语法**

初始化Queen对象时，若括号没有指定最大可接收消息数目或消息数目为负值，那就代表可接收的消息数没有上限（除非内存使用完）。

常用方法介绍:

- qsize()：消息队列的长度。
- put(msg, block, timeout)：试图插入消息队列，超时抛错。
- block默认为True，如果使用默认值，且没有设置timeout，消息队列已满，那么程序将处于阻塞状态（停在等待写入状态），直到从消息队列腾出空间为止。如果设置了timeout，则会等待timeout秒，若还没获取到空间就抛错。
- put_nowait(msg)：立即插入消息，已满报错。put_nowait(item)==put(item, False)；
- full()：消息队列是否已满。
- empty()：消息队列是否为空。
- get(block, timeout)：试图获取消息，超时抛错。
	- block默认为True，如果使用默认值，且没有设置timeout，消息队列为空，那么程序将处于阻塞状态（停在读取状态），直到从消息队列中读到消息为止。如果设置了timeout，则会等待timeout秒，若还没获取到就抛错。
	- block为False，消息队列为空，则会立即抛出异常。
- get_nowait(msg)：立即获取消息，异常报错。get_nowait()==get(False)

简单跑跑。

	from multiprocessing import Queue, Process
	from time import sleep
	import random
	
	msg_queen = Queue(5)
	
	
	def wq(msg_q):
	    while True:
	        if not msg_q.full():
	            msg_q.put_nowait('put data')
	            sleep(random.random())
	            print('put data into queue')
	        else:
	            break
	
	
	def rq(msg_q):
	    while True:
	        if not msg_q.empty():
	            data = msg_q.get_nowait()
	            sleep(random.random())
	            print(data)
	        else:
	            break
	
	
	if __name__ == '__main__':
	    wq_process = Process(target=wq, args=(msg_queen, ))
	    wq_process.start()
	    sleep(random.random())
	    # wq_process.join()
	    rq_process = Process(target=rq, args=(msg_queen, ))
	    rq_process.start()
	    # rq_process.join()

## 2.5 进程池

当需要创建的子进程数量不多的时候，可以直接利用multiprocessing中的Process去动态创建多个进程，但是如果要创建成百上千个目标，手动去创建的进程的工作量较大，此时就可以用到multiprocessing模块提供的Pool方法。

初始化进程池，可以制定一个最大进程数，当有新的请求提交到Pool中时，如果池还没满，就会创建一个新的进程来执行这个请求；如果进程池的数目已经达到最大值，那么该请求就会等待，指导进程池中的进程结束，才会用**之前的进程**来执行新的任务。

	from multiprocessing import Pool
	import time
	import random
	import os
	
	
	def work_pool(msg):
	    t_start = time.time()
	    print('this num of the process is %s' % msg)
	    print('this pid of the process is %s' % os.getpid())
	    print('this ppid of the process is %s' % os.getppid())
	    time.sleep(random.random()*10)
	    t_stop = time.time()
	    print('spend time %d' % int(t_stop-t_start))
	
	
	if __name__ == '__main__':
	    process_pool = Pool(5)
	    for i in range(10):
	        process_pool.apply_async(work_pool, (i, ))
	    process_pool.close()
	    process_pool.join()

结果：

	this num of the process is 0
	this pid of the process is 8144
	this ppid of the process is 6396
	this num of the process is 1
	this pid of the process is 8596
	this ppid of the process is 6396
	this num of the process is 2
	this pid of the process is 6464
	this ppid of the process is 6396
	this num of the process is 3
	this pid of the process is 6240
	this ppid of the process is 6396
	this num of the process is 4
	this pid of the process is 7300
	this ppid of the process is 6396
	spend time 3
	this num of the process is 5
	this pid of the process is 8596
	this ppid of the process is 6396
	spend time 3
	this num of the process is 6
	this pid of the process is 7300
	this ppid of the process is 6396
	spend time 6
	this num of the process is 7
	this pid of the process is 8144
	this ppid of the process is 6396
	spend time 2
	this num of the process is 8
	this pid of the process is 7300
	this ppid of the process is 6396
	spend time 7
	this num of the process is 9
	this pid of the process is 6464
	this ppid of the process is 6396
	spend time 4
	spend time 9
	spend time 3
	spend time 6
	spend time 7

可以看出是重复利用进程的，且进程之间互不影响。

**Pool常用函数解析：**

- apply_async(func[, args[, kwargs]])：非阻塞方式调用func（并行执行，阻塞方式必须等待上一个进程完了才能执行下一个进程），args为参数列表，元组形式；kwargs是命名参数字典。
- close()：关闭进程池，不再接受其它任务。
- terminate()：不管任务是否完成，立即终止。
- join()：主进程阻塞，等待子进程结束退出，**必须在close或terminate之后才能调用**。

**进程池中的Queue：**

如果要使用Pool创建进程，就需要使用mutilprocessing.Manage().Queue()，而不是multiprocessing.Queue()，否则会得到一条如下的错误信息：	

	RuntimeError: Queue objects should only be shared between processes through inheritance.

下面的实例演示了进程池中的进程如何通信：

	from multiprocessing import Pool, Manager
	import time
	import random
	import os
	
	
	def write_p(msg):
	    for i in 'daocoder':
	        msg.put(i)
	        print('process id is %s' % os.getpid())
	        print('parent process id is %s' % os.getppid())
	    time.sleep(random.random())
	
	
	def read_p(q):
	    for i in range(q.qsize()):
	        char_name = q.get()
	        print(char_name)
	        print('process id is %s' % os.getpid())
	        print('parent process id is %s' % os.getppid())
	    time.sleep(random.random())
	
	
	if __name__ == '__main__':
	    q = Manager().Queue()
	    process_pool = Pool()
	    process_pool.apply_async(write_p, (q, ))
	    time.sleep(random.random())
	    process_pool.apply_async(read_p, (q, ))
	    process_pool.close()
	    process_pool.join()

结果：

	process id is 6532
	parent process id is 7968
	process id is 6532
	parent process id is 7968
	process id is 6532
	parent process id is 7968
	process id is 6532
	parent process id is 7968
	process id is 6532
	parent process id is 7968
	process id is 6532
	parent process id is 7968
	process id is 6532
	parent process id is 7968
	process id is 6532
	parent process id is 7968
	d
	process id is 4436
	parent process id is 7968
	a
	process id is 4436
	parent process id is 7968
	o
	process id is 4436
	parent process id is 7968
	c
	process id is 4436
	parent process id is 7968
	o
	process id is 4436
	parent process id is 7968
	d
	process id is 4436
	parent process id is 7968
	e
	process id is 4436
	parent process id is 7968
	r
	process id is 4436
	parent process id is 7968

# 3、协程

## 3.1 迭代器

迭代是一种访问集合方式的一种方式。迭代器是可以记住其遍历对象的位置的对象。迭代器对象从集合的第一个元素开始访问，直到所有的元素被访问完结束，迭代器只能前进不能后退。

### 3.1.1 可迭代对象

在py中，有我们已知的list、tuple、str等类型的数据使用for…in…的循环语法从其中拿到数据进行使用，我们称这样的过程为遍历、也叫迭代。

那么问题来了，为什么有的数据类型可以用for…in…进行迭代，而有的数据不行。

	for i in 100:
	    print(i)
	Traceback (most recent call last):
	  File "C:\software\python\lib\site-packages\IPython\core\interactiveshell.py", line 2910, in run_code
	    exec(code_obj, self.user_global_ns, self.user_ns)
	  File "<ipython-input-2-bcddcd506fd8>", line 1, in <module>
	    for i in 100:
	TypeError: 'int' object is not iterable

整型对象不是可迭代的。

	from collections import Iterable


	class Mylist(object):
	    def __init__(self):
	        self.container = []
	
	    def add(self, element):
	        self.container.append(element)
	
	
	mylist = Mylist()
	mylist.add(1)
	mylist.add(2)
	mylist.add(3)
	
	for i in mylist:
	    print(i)

	Traceback (most recent call last):
	  File "D:/python/demo/thread.py", line 22, in <module>
	    for i in mylist:
	TypeError: 'Mylist' object is not iterable

我们自定义一个容器类型，里面存放了3个数据，尝试去遍历它，发现报错。即这个自定义对象也是不可以遍历的。**那么如何判断一个对象是否是可以遍历的？**

### 3.1.2 判断对象是否可以遍历（迭代）

我们可以通过for…in…这类语句迭代读取一条数据的对象称之为可迭代对象（Iterable）。

可以使用instance()判断一个对象是否是Iterable对象。

以上面的mylist为例。

	print(isinstance(mylist, Iterable))
	print(isinstance([], Iterable))
	print(isinstance({}, Iterable))
	print(isinstance(100, Iterable))
	print(isinstance('daocoder', Iterable))

结果：

	False
	True
	True
	False
	True

### 3.1.3 可迭代对象的本质

我们从表面去看，对可迭代对象来说，每迭代一次都会返回下一个元素，直到这个对象遍历完毕。那么在这个过程中就应该有一个“变量”在记录每次迭代后当前的位置，以便下次都可以获取到下一条数据。我们称这个变量为迭代器（iterator）。

**可迭代对象的本质就是可以向我们提供一个这样的“变量”，即迭代器帮助我们去进行迭代遍历使用。**

**可迭代对象通过__iter()__方法向我们提供一个迭代器，我们在迭代一个可迭代对象时，实际上就是获取该对象提供的迭代器，然后通过这个迭代器依次获取该对象的每个数据。**

那么就可以这么说，**一个具备__iter()__方法的对象就是可迭代对象。**

还是上面mylist那个自定义对象，添加如下代码：

    def __iter__(self):
        pass

运行：

	print(isinstance(mylist, Iterable))

结果：

	True

那么按道理来说，mylist就可以遍历了才是，如下：

	for i in mylist:
	    print(i)

结果：

	Traceback (most recent call last):
	True
	  File "D:/python/demo/thread.py", line 24, in <module>
	    for i in mylist:
	TypeError: iter() returned non-iterator of type 'NoneType'

### 3.1.4 iter()和next()函数

list、tuple等都是可迭代对象，我们可以通过iter()函数获取这些可迭代对象的迭代器，然后我们可以通过获取迭代器的next()函数来获取下一个数据。iter()函数实际上就是调用了可迭代对象的__iter__方法。

	test = [1, 2, 3, 4, 5]
	list_iter = iter(test)
	print(next(list_iter))
	print(next(list_iter))
	print(next(list_iter))
	print(next(list_iter))
	print(next(list_iter))
	print(next(list_iter))

结果：

	1
	2
	3
	4
	5
	Traceback (most recent call last):
	  File "D:/python/demo/thread.py", line 34, in <module>
	    print(next(list_iter))
	StopIteration

当我们迭代完最后一个数据之后，再次调用next()函数就会抛出StopIteration的异常，说明我们所有的数据都已经迭代完成，不需要再执行next()函数了。

### 3.1.5 如何判断一个对象是否是迭代器

可以使用isinstance()判断一个对象是否是Iterator对象。

	print(isinstance('daocoder', Iterator))
	print(isinstance(iter('daocoder'), Iterator))
	print(isinstance(123, Iterator))
	print(isinstance(iter(123), Iterator))

结果：

	False
	True
	False
	Traceback (most recent call last):
	  File "D:/python/demo/thread.py", line 30, in <module>
	    print(isinstance(iter(123), Iterator))
	TypeError: 'int' object is not iterable

### 3.1.6 迭代器Iterator

从上面的一步步走过来，我们清楚迭代器是帮我们记录每次迭代到访问的位置，当我们对迭代器使用next()函数的时候，迭代器会向我们返回记录它的下一个数据的位置。实际上，使用next()函数的时候，其调用的就是迭代器对象的__next__方法。但这还不够，python要求迭代器本身也是可迭代的，所以还要为迭代器实现__iter__方法，而__iter__要返回一个迭代器，迭代器自身就是一个迭代器，所以返回其自身就好。

简而言之，**一个实现了__iter__和__next__方法的对象就是迭代器。**

然后上面的自定义可以写成这样。

	class Mylist(object):
	    def __init__(self):
	        self.container = []
	
	    def add(self, element):
	        self.container.append(element)
	
	    def __iter__(self):
	        return MyIterator(self)
	
	
	class MyIterator(object):
	    def __init__(self, outlist):
	        self.mylist = outlist
	        self.current = 0
	
	    def __iter__(self):
	        return self
	
	    def __next__(self):
	        if self.current < len(self.mylist.container):
	            item = self.mylist.container[self.current]
	            self.current += 1
	            return item
	        else:
	            raise StopIteration
	
	
	if __name__ == '__main__':
	    mylist = Mylist()
	    mylist.add(1)
	    mylist.add(2)
	    mylist.add(3)
	    mylist.add(4)
	    mylist.add(5)
	    for num in mylist:
	        print(num)

### 3.1.7 for…in…循环的本质

`for item in iterable` 循环的本质就是先通过iter()获取可迭代对象Iterable的迭代器，然后不断调用next()方法来获取下一个值并将其复制给item，当遇到StopIteration的异常后循环结束。

### 3.1.8 迭代器的应用场景

迭代器的核心功能是可以通过next()函数的调用来返回下一个数据值。如果每次返回的数据值不是在已有数据集合中读取的，而是通过一定的规律生成的，那么也就意味着可以不用再依赖一个已有的数据集合，即不用再将所有需要迭代的数据一次性缓存下来供后续依次读取，这样就可以节省大量内存。

下面利用迭代器实现兔子数列（斐波那契数列）。

	class FibIterator(object):
	    def __init__(self, n):
	        self.n = n
	        self.current = 0
	        self.num1 = 0
	        self.num2 = 1
	
	    def __iter__(self):
	        return self
	
	    def __next__(self):
	        if self.current < self.n:
	            num = self.num1
	            self.num1, self.num2 = self.num2, self.num1+self.num2
	            self.current += 1
	            return num
	        else:
	            raise StopIteration
	
	
	if __name__ == '__main__':
	    fib = FibIterator(5)
	    for i in range(6):
	        print(next(fib))

结果为：

	0
	1
	1
	2
	3
	Traceback (most recent call last):
	  File "D:/python/demo/thread.py", line 29, in <module>
	    print(next(fib))
	  File "D:/python/demo/thread.py", line 23, in __next__
	    raise StopIteration
	StopIteration

## 3.2 生成器

利用迭代器，我们可以在每次迭代获取数据（利用迭代器的next方法）时按照特定的规律进行生成。但我们在实现一个迭代器时，关于当前迭代的状态需要我们自己去记录，进而才能依据当前状态去生成下一个数据。为了达到记录当前状态，并配合next()函数进行迭代使用，我们可以采用更简洁的用法，即生成器generator()。

### 3.2.1 创建生成器

**1、利用生成器符号**

列表生成式的[]改成()。

	L = [i for i in range(6)]
	print(L)
	
	G = (i for i in range(6))
	print(G)

结果：

	[0, 1, 2, 3, 4, 5]
	<generator object <genexpr> at 0x0000000001E98308>

创建L和G的区别仅在于最外层的()和[]，L是一个列表，G是一个生成器。我们可以直接打印L的每个元素，对于生成器G，我们可以按照迭代器的使用方法来使用，即可以通过next()函数、for循环、list()等方法使用。

	L = [i for i in range(6)]
	print(L)
	
	G = (i for i in range(6))
	print(G)
	
	# print(next(G))
	# print(next(G))
	# print(next(G))
	# print(next(G))
	# print(next(G))
	# print(next(G))
	
	for j in G:
	    print(j)

结果为：

	[0, 1, 2, 3, 4, 5]
	<generator object <genexpr> at 0x0000000001F08308>
	0
	1
	2
	3
	4
	5

**2、yield**

generator非常强大。如果推算的算法比较复杂，用类似列表生成式的for循环无法实现的时候，还可以用函数来实现。

	def fib(n):
	    current = 0
	    num1 = 0
	    num2 = 1
	    while current < n:
	        current += 1
	        num = num1
	        num1, num2 = num2, num1 + num2
	        yield num
	    return 'done'
	
	
	for i in fib(6):
	    print(i)

结果:

	0
	1
	1
	2
	3
	5

在使用生成器实现的方式中，我们将原本在迭代器中__next__方法中实现的基本逻辑放到一个函数中实现，现在将每次迭代器返回数值的return换成了yield，此时定义的函数就不再是函数，而是一个生成器。**简单来说：只要有yield关键字的就称为生成器。**

但是用for循环调用generator时，发现拿不到generator的return语句的返回值。**如果想获取返回值，必须捕获StopIteration错误，返回值包含在StopIteration的value中。**

	def fib(n):
	    current = 0
	    num1 = 0
	    num2 = 1
	    while current < n:
	        current += 1
	        num = num1
	        num1, num2 = num2, num1 + num2
	        yield num
	    return 'done'
	
	
	G = fib(5)
	while True:
	    try:
	        n = next(G)
	        print(n)
	    except StopIteration as se:
	        print(se.value)
	        break

结果：

	0
	1
	1
	2
	3
	done

总结：

- 试用了yield关键字的函数就不再是函数，而是生成器。
- yield作用有两点：保存当前的运行状态（断点），然后暂停执行，即生成器被挂起；将yield关键字后面表达式的值作为返回值返回，此时可以理解为起到了return作用。
- 使用next()函数可以生成器从断点处继续执行，即唤醒生成器（函数）。
- py3中的生成器可以使用return返回最终运行的返回值，而py2中的生成器不允许使用个return返回一个返回值（可以使用return语句从生成器中退出，但是不能return后面不能有任何表达式）。

### 3.2.2 使用send唤醒

除了上面利用next()函数来唤醒生成器继续执行外，还可以使用send()函数来唤醒其继续执行。使用send()函数的另一个好处是可以同时向断点处附加一个数据。

	def fib(n):
	    i = 0
	    while i < n:
	        temp = yield i
	        print(temp)
	        i += 1
	
	
	G = fib(5)
	
	print(next(G))
	print(G.__next__())
	print(G.send('daocoder'))
	print(next(G))

结果：

	0
	None
	1
	daocoder
	2
	None
	3

执行到yield时，G函数暂存当前状态，返回i的值；temp接收下次G.send('daocoder')，next(G)===G.__next__()===G.send(None)。

## 3.3 协程

协程又称为微线程，纤程，英文为coroutine。

### 3.3.1 协程简介

协程是py中实现多任务的另一种方式，只不过比线程占用更小的资源，且切换上线文更快。

通俗的理解就是：**在一个线程的某个函数，可以在任何地方保存当前函数的一些临时变量等信息，谈后切换到另一个函数中执行，注意这里不是通过调用函数的方式去做到的，并且切换的次数以及什么时候切换到原来的函数都由开发者决定。**

### 3.3.2 yield

	import time
	
	
	def work1():
	    while True:
	        print('work1')
	        yield
	        time.sleep(0.5)
	
	
	def work2():
	    while True:
	        print('work2')
	        yield
	        time.sleep(0.5)
	
	
	if __name__ == '__main__':
	    w1 = work1()
	    w2 = work2()
	    while True:
	        next(w1)
	        next(w2)

结果为：

	work1
	work2
	work1
	work2
	work1
	work2

### 3.3.3 greenlet

为了更好的使用协程来完成任务，py提供了greenlet对其封装，从而使切换任务变得更加简单。

	import time
	from greenlet import greenlet
	
	
	def work1():
	    while True:
	        print('work1')
	        w2.switch()
	        time.sleep(0.5)
	
	
	def work2():
	    while True:
	        print('work2')
	        w1.switch()
	        time.sleep(0.5)
	
	
	if __name__ == '__main__':
	    w1 = greenlet(work1)
	    w2 = greenlet(work2)
	    w1.switch()

结果为：

	work1
	work2
	work1
	work2
	work1
	work2

### 3.3.3 gevent

greenlet已经实现了协程，但是如上面代码所示，它还需要人工进行切换，由此py提供了一个更强大的封装gevent，它能够自动切换任务。

其原理是当一个greenlet遇到一个IO（网络、文件等输入输出操作）时，就自动切换到其它的greenlet，等到IO操作完成，再在适当的条件下切回来继续执行。

由于IO操作非常耗时，经常使程序处于等待状态，有了gevent为我们自动切换协程，就保证总有greenlet在运行，而不是等待IO。

**1、无IO操作等待**

	import gevent
	
	
	def work(n):
	    for i in range(n):
	        print('num is %s, current greenlet is %s' % (i, gevent.getcurrent()))
	
	
	g1 = gevent.spawn(work, 5)
	g2 = gevent.spawn(work, 4)
	g3 = gevent.spawn(work, 3)
	g1.join()
	g2.join()
	g3.join()

结果是：

	num is 0, current greenlet is <Greenlet at 0x2bf6898: work(5)>
	num is 1, current greenlet is <Greenlet at 0x2bf6898: work(5)>
	num is 2, current greenlet is <Greenlet at 0x2bf6898: work(5)>
	num is 3, current greenlet is <Greenlet at 0x2bf6898: work(5)>
	num is 4, current greenlet is <Greenlet at 0x2bf6898: work(5)>
	num is 0, current greenlet is <Greenlet at 0x2bf69c8: work(4)>
	num is 1, current greenlet is <Greenlet at 0x2bf69c8: work(4)>
	num is 2, current greenlet is <Greenlet at 0x2bf69c8: work(4)>
	num is 3, current greenlet is <Greenlet at 0x2bf69c8: work(4)>
	num is 0, current greenlet is <Greenlet at 0x2bf6a60: work(3)>
	num is 1, current greenlet is <Greenlet at 0x2bf6a60: work(3)>
	num is 2, current greenlet is <Greenlet at 0x2bf6a60: work(3)>

可以看出3个greenlet是依次执行而不是顺序执行。

**2、有IO操作等待（gevent.sleep）**

	import gevent
	
	
	def work(n):
	    for i in range(n):
	        print('num is %s, current greenlet is %s' % (i, gevent.getcurrent()))
	        gevent.sleep(0.5)
	
	
	g1 = gevent.spawn(work, 5)
	g2 = gevent.spawn(work, 4)
	g3 = gevent.spawn(work, 3)
	g1.join()
	g2.join()
	g3.join()

结果：

	num is 0, current greenlet is <Greenlet at 0x2bc5898: work(5)>
	num is 0, current greenlet is <Greenlet at 0x2bc59c8: work(4)>
	num is 0, current greenlet is <Greenlet at 0x2bc5a60: work(3)>
	num is 1, current greenlet is <Greenlet at 0x2bc5898: work(5)>
	num is 1, current greenlet is <Greenlet at 0x2bc5a60: work(3)>
	num is 1, current greenlet is <Greenlet at 0x2bc59c8: work(4)>
	num is 2, current greenlet is <Greenlet at 0x2bc5898: work(5)>
	num is 2, current greenlet is <Greenlet at 0x2bc59c8: work(4)>
	num is 2, current greenlet is <Greenlet at 0x2bc5a60: work(3)>
	num is 3, current greenlet is <Greenlet at 0x2bc5898: work(5)>
	num is 3, current greenlet is <Greenlet at 0x2bc59c8: work(4)>
	num is 4, current greenlet is <Greenlet at 0x2bc5898: work(5)>

这里发现greenlet遇到其耗时操作时，自动切换协程。

**3、有IO操作等待（time.sleep）**

	import gevent
	import time
	
	
	def work(n):
	    for i in range(n):
	        print('num is %s, current greenlet is %s' % (i, gevent.getcurrent()))
	        time.sleep(0.5)
	
	
	g1 = gevent.spawn(work, 5)
	g2 = gevent.spawn(work, 4)
	g3 = gevent.spawn(work, 3)
	g1.join()
	g2.join()
	g3.join()

结果：

	num is 0, current greenlet is <Greenlet at 0x2bc5898: work(5)>
	num is 1, current greenlet is <Greenlet at 0x2bc5898: work(5)>
	num is 2, current greenlet is <Greenlet at 0x2bc5898: work(5)>
	num is 3, current greenlet is <Greenlet at 0x2bc5898: work(5)>
	num is 4, current greenlet is <Greenlet at 0x2bc5898: work(5)>
	num is 0, current greenlet is <Greenlet at 0x2bc59c8: work(4)>
	num is 1, current greenlet is <Greenlet at 0x2bc59c8: work(4)>
	num is 2, current greenlet is <Greenlet at 0x2bc59c8: work(4)>
	num is 3, current greenlet is <Greenlet at 0x2bc59c8: work(4)>
	num is 0, current greenlet is <Greenlet at 0x2bc5a60: work(3)>
	num is 1, current greenlet is <Greenlet at 0x2bc5a60: work(3)>
	num is 2, current greenlet is <Greenlet at 0x2bc5a60: work(3)>

这里我们发现，time模块的耗时并没有使其自动切换上下文。

**4、有IO操作等待（利用monkey）**

	import gevent
	from gevent import monkey
	import time
	
	
	monkey.patch_all()
	
	
	def work(n, *args):
	    for i in range(n):
	        print('name is %s, current greenlet is %s' % (args[0], gevent.getcurrent()))
	        time.sleep(0.5)
	
	
	g1 = gevent.spawn(work, 5, 'g1')
	g2 = gevent.spawn(work, 4, 'g2')
	g3 = gevent.spawn(work, 3, 'g3')
	g1.join()
	g2.join()
	g3.join()

结果：

	num is 0, current greenlet is <Greenlet at 0x30590e0: work(5)>
	num is 0, current greenlet is <Greenlet at 0x3059210: work(4)>
	num is 0, current greenlet is <Greenlet at 0x30592a8: work(3)>
	num is 1, current greenlet is <Greenlet at 0x30590e0: work(5)>
	num is 1, current greenlet is <Greenlet at 0x30592a8: work(3)>
	num is 1, current greenlet is <Greenlet at 0x3059210: work(4)>
	num is 2, current greenlet is <Greenlet at 0x30590e0: work(5)>
	num is 2, current greenlet is <Greenlet at 0x3059210: work(4)>
	num is 2, current greenlet is <Greenlet at 0x30592a8: work(3)>
	num is 3, current greenlet is <Greenlet at 0x30590e0: work(5)>
	num is 3, current greenlet is <Greenlet at 0x3059210: work(4)>
	num is 4, current greenlet is <Greenlet at 0x30590e0: work(5)>

另一种写法：

	import gevent
	from gevent import monkey
	import time
	
	
	monkey.patch_all()
	
	
	def work(n, *args):
	    for i in range(n):
	        print('name is %s, current greenlet is %s' % (args[0], gevent.getcurrent()))
	        time.sleep(0.5)
	
	
	gevent.joinall([
	    gevent.spawn(work, 5, 'g1'),
	    gevent.spawn(work, 4, 'g2'),
	    gevent.spawn(work, 3, 'g3')
	])

结果为：

	name is g1, current greenlet is <Greenlet at 0x30680e0: work(5, 'g1')>
	name is g2, current greenlet is <Greenlet at 0x3068210: work(4, 'g2')>
	name is g3, current greenlet is <Greenlet at 0x30682a8: work(3, 'g3')>
	name is g1, current greenlet is <Greenlet at 0x30680e0: work(5, 'g1')>
	name is g3, current greenlet is <Greenlet at 0x30682a8: work(3, 'g3')>
	name is g2, current greenlet is <Greenlet at 0x3068210: work(4, 'g2')>
	name is g1, current greenlet is <Greenlet at 0x30680e0: work(5, 'g1')>
	name is g2, current greenlet is <Greenlet at 0x3068210: work(4, 'g2')>
	name is g3, current greenlet is <Greenlet at 0x30682a8: work(3, 'g3')>
	name is g1, current greenlet is <Greenlet at 0x30680e0: work(5, 'g1')>
	name is g2, current greenlet is <Greenlet at 0x3068210: work(4, 'g2')>
	name is g1, current greenlet is <Greenlet at 0x30680e0: work(5, 'g1')>







