# coding = utf-8
# coding = utf-8
import re
import sys

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from queue import Queue
import threading
import os
from optparse import OptionParser


# 爬取https://www.89ip.cn/ 的代理ip和端口
class Ip_port_get(object):
    def __init__(self, thread_count):
        self._base_url = "https://www.89ip.cn/"
        self._queue = Queue()  # 存放要爬取的页面的网址
        self._ua = UserAgent()  # 随机ua
        self._threads = []  # 多线程集合
        self._result = []  # 结果集
        self._thread_count = thread_count  # 线程数
        self._total_count = 0  # 队列的长度

    def init_pages(self):
        """
        初始化需要爬取的地址
        :return:
        """
        for i in range(1, 24):
            url_page = self._base_url + f"index_{i}.html"
            self._queue.put(url_page)
        # 保存总的长度
        self._total_count = self._queue.qsize()

    # 启动
    def start(self):
        print("开始爬取。。。。")
        self.init_pages()
        for i in range(self._thread_count):
            # 设置线程
            self._threads.append(self.Ip_thread(self._queue, self._ua, self._result, self._total_count))
        # 启动线程
        for t in self._threads:
            t.start()
        for t in self._threads:
            t.join()

        # 处理结果
        self._result = list(set(self._result))
        if os.path.exists("./proxy_ip.txt"):
            os.remove("./proxy_ip.txt")
        with open("./proxy_ip.txt", "w") as f:
            for i in self._result:
                f.write(i + "\n")

    class Ip_thread(threading.Thread):
        """
        内部类 ：专用于多线程
        """

        def __init__(self, queue, ua, result, total_count):
            super().__init__()
            self._queue = queue
            self._ua = ua
            self._result = result
            self._total_count = total_count

        # 显示进度
        def msg(self):
            """
            显示进度
            :return:
            """
            # 总的进度
            already_do = round((100 - (self._queue.qsize() / self._total_count) * 100), 2)
            count = int(already_do)
            sys.stdout.write("\r" + ("=" * count) + f"[{already_do}%]")

        def run(self):
            while not self._queue.empty():
                url = self._queue.get()
                headers = {
                    "User-Agent": self._ua.random
                }
                # 显示进度
                self.msg()
                response = requests.get(url, headers=headers)
                html = response.text
                soup = BeautifulSoup(html, "lxml")
                tbody = soup.find("tbody")
                trs = tbody.find_all("tr")
                for tr in trs:
                    tds = tr.find_all("td")
                    ipt = tds[0].string
                    ipt = re.sub("[\n\t]", "", ipt)
                    port = tds[1].string
                    port = re.sub("[\n\t]", "", port)
                    ip_port = ipt + ":" + port
                    # 验证ip是否有用
                    url_test = "http://httpbin.org/ip"
                    proxy = {
                        "http": f"http://{ip_port}",
                        "https": f"http://{ip_port}"
                    }
                    try:
                        res = requests.get(url_test, proxies=proxy, timeout=2)
                        # 判断是否有效
                        res_str = res.text
                        if ipt in res_str:
                            self._result.append(ip_port)
                    except Exception as e:
                        pass


if __name__ == '__main__':
    """
    用命令执行python爬虫,传递一个参数，线程
    """
    parse = OptionParser()
    parse.add_option("-t", "--thread_count", dest="thread_count", type=int, help="设置线程的数量")
    options, args = parse.parse_args()
    if options.thread_count:
        ipPort = Ip_port_get(options.thread_count)
        ipPort.start()
    else:
        parse.print_help()
        sys.exit(0)
