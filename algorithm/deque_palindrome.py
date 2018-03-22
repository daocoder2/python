#! /usr/bin/python
# -*- coding:utf-8 -*-

from pythonds.basic.deque import Deque


def palchecker(astring):
    chardeque = Deque()
    for ch in astring:
        chardeque.addRear(ch)
    still_equal = True
    while chardeque.size() > 1 and still_equal:
        first = chardeque.removeFront()
        last = chardeque.removeRear()
        if first != last:
            still_equal = False
    return still_equal


print(palchecker("lsdkjfskf"))
print(palchecker("radar"))



