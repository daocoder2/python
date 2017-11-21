#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
import urllib.request
import urllib.error
import threading
import queue
import time

# FILE_LOCK = threading.Lock() # 锁对象、没用到
SHARE_Q = queue.Queue()  # 构造一个不限制大小的的队列
THREAD_MAX_NUM = 3  # 设置线程的个数
RES_DATA = []


class MyThread(threading.Thread):
    def __init__(self, func):
        super(MyThread, self).__init__()  # 调用父类的构造函数
        self.func = func  # 传入线程函数逻辑

    def run(self):
        self.func()


def worker():
    global SHARE_Q
    while not SHARE_Q.empty():
        url = SHARE_Q.get()  # 获得任务
        page_content = get_page(url)
        find_title(page_content)  # 获得当前页面的电影名
        # write_into_file(tempRES_DATA)
        time.sleep(1)
        SHARE_Q.task_done()


def get_page(url):
    """根据所给的url爬取网页HTML
    Args: 
        url: 表示当前要爬取页面的url
    Returns:
        返回抓取到整个页面的HTML
    Raises:
        urllib.error:url引发的异常
    """
    page_content = ''
    try :
        page_content = urllib.request.urlopen(url).read().decode("utf-8")
    except urllib.error.HTTPError as e:
        print(e)
        if hasattr(e, "code"):
            print(e.getcode())
            # HTTP Error %s: %s' % (e.code, e.msg)
        elif hasattr(e, "reason"):
            print(e.reason)
    return page_content


def find_title(page_content):
    """通过返回的整个网页HTML, 正则匹配前100的电影名称
    Args:
        page_content: 传入页面的HTML文本用于正则匹配
    """
    tempRES_DATA = []
    movie_items = re.findall(r'<span\s?class="title">(.*?)</span>', page_content, re.S)
    for index, item in enumerate(movie_items):
        if item.find("&nbsp") == -1:
            tempRES_DATA.append(item)
    RES_DATA.append(tempRES_DATA)


def main():
    # 全局先进先出队列
    global SHARE_Q
    threads = []
    douban_url = "http://movie.douban.com/top250?start={page}"
    # 向队列中放入任务, 真正使用时, 应该设置为可持续的放入任务
    for index in range(10):   
        SHARE_Q.put(douban_url.format(page = index * 25))
    # 先创建线程对象
    for i in range(THREAD_MAX_NUM):
        thread = MyThread(worker)
        # thread.start()  # 线程开始处理任务
        threads.append(thread)
    # 启动所有线程
    for t in threads:
        t.start()
    # 等待至线程中止
    for thread in threads :
        thread.join()
    # 等待至队列为空再执行文件写入的动作
    SHARE_Q.join()
    with open("movie.txt", "w+") as my_file :
        for page in RES_DATA :
            for movie_name in page:
                my_file.write(movie_name + "\n")
    print("Spider Successful!")


if __name__ == '__main__':
    main()
