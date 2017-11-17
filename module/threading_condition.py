#!/usr/bin/python
# -*- coding:utf-8 -*-

'''
下文主要是对threading.Condition的说明
Python提供的Condition对象提供了对复杂线程同步问题的支持。
Condition被称为条件变量，除了提供与Lock类似的acquire和release方法外，还提供了wait和notify方法。
线程首先acquire一个条件变量，然后判断一些条件。如果条件不满足则wait；（等待重新进行条件判断。）
如果条件满足，进行一些处理改变条件后，通过notify方法通知其他线程，其他处于wait状态的线程接到通知后会重新判断条件。
不断的重复这一过程，从而解决复杂的同步问题。

经典的生产者与消费者问题：假设有一群生产者(Producer)和一群消费者（Consumer）通过一个市场来交互产品。
生产者的”策略“是如果市场上剩余的产品少于5个，那么就生产1个产品放到市场上；
而消费者的”策略“是如果市场上剩余产品的数量多余5个，那么就消费1个产品。

再借鉴一个地址来说明：http://python.jobbole.com/82742/

执行效果：
Market is Empty...
Producer: 2
Producer have producted something
'''

import threading
import random, time


MAX_SIZE = 5
SHARE_Q = []  # 模拟共享队列
condition = threading.Condition()


class Producer(threading.Thread):
    def __init__(self):
        super(Producer, self).__init__()

    def run(self):
        products = range(MAX_SIZE)
        global SHARE_Q
        while True:
            condition.acquire()
            if len(SHARE_Q) == MAX_SIZE:
                print("Market is full..")
                # 先是市场产品饱满、然后等待消费者在市场消费产品、等通知后这里回归继续执行、再重新判断条件
                condition.wait()
                print("Consumer have comsumed something")
            else:
                product = random.choice(products)
                SHARE_Q.append(product)
                print("Producer: ", product)
                condition.notify()
            condition.release()
            time.sleep(random.random())


class Consumer(threading.Thread):
    def __init__(self):
        super(Consumer, self).__init__()

    def run(self):
        global SHARE_Q
        while True:
            condition.acquire()
            if not SHARE_Q:
                print("Market is Empty...")
                # 先是市场产品为空、然后等待生产者向市场投入产品、等通知后这里回归继续执行、再重新判断条件
                condition.wait()
                print("Producer have producted something")
            else:
                product = SHARE_Q.pop(0)
                print("Consumer:", product)
                condition.notify()
            condition.release()
            time.sleep(random.random())


def main():
    producer = Producer()
    consumer = Consumer()
    producer.start()
    consumer.start()


if __name__ == '__main__':
    main()
