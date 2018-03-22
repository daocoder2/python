#! /usr/bin/python
# -*- coding:utf-8 -*-

from pythonds.basic.queue import Queue


def hot_potato(namelist, num):
    simqueue = Queue()
    for name in namelist:
        simqueue.enqueue(name)
    while simqueue.size() > 1:
        for i in range(num):
            simqueue.enqueue(simqueue.dequeue())
        test = simqueue.dequeue()
        print(test)
    return simqueue.dequeue()


print(hot_potato(['Bill', 'David', 'Susan', 'Jane', 'Kent', 'Brad'], 7))
