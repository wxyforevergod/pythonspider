# coding = utf-8
import threading

import requests
import sys
from queue import Queue
# 设置环境变量
sys.path.append("../")
from config import domain_dict_path
from common import *


class Burp_list(object):
    def __init__(self, domain, thread_count):
        self._domain = domain
        self._queue = Queue()
        self._result = []
        self._threads = []
        self._thread_count = thread_count

    # 初始化队列
    def _queue_init(self):
        with open(domain_dict_path, "r") as f:
            # 拼接域名
            for d in f:
                scan_domain = d.strip()+"."+self._domain
                self._queue.put("http://"+scan_domain)

    def start(self):
        print("burp模块开始获取子域名")
        # 初始化队列
        self._queue_init()
        # 准备线程
        for i in range(self._thread_count):
            self._threads.append(self.Dict_thread(self._queue, self._result))
        # 启动线程
        for t in self._threads:
            t.start()
        for t in self._threads:
            t.join()
            # 保存结果
        save(data=self._result, module="brute", domain=self._domain)
        print("brute模块运行完成！")



    class Dict_thread(threading.Thread):
        def __init__(self, queue, result):
            super().__init__()
            self._queue = queue
            self._result = result

        def run(self):
            while not self._queue.empty():
                scan_domain = self._queue.get()
                try:
                    response = get_url(scan_domain)
                    if response.status_code != 404:
                        # 存放在一个result
                        self._result.append(scan_domain.lstrip("http://"))
                except Exception as e:
                    pass



