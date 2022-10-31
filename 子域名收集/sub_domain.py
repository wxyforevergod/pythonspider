# coding = utf-8
# coding = utf-8
"""
子域名收集的启动程序
"""
import sys

from modules.crt import Domain_crt
from modules.burp import Burp_list
import threading
from common import out_put
from optparse import OptionParser

domain = "wuyecao.net"

if __name__ == '__main__':
    """
    用命令执行python爬虫,传递一个参数，线程
    """
    parse = OptionParser()
    parse.add_option("-d", "--domain", dest="domain", help="设置domain")
    parse.add_option("-t", "--thread_count", dest="thread_count", type=int, help="设置线程的数量")
    options, args = parse.parse_args()
    if options.thread_count and options.domain:
        crt = Domain_crt(options.domain)
        brup = Burp_list(options.domain, options.thread_count)
        # 利用线程启动
        threads = [threading.Thread(target=crt.start), threading.Thread(target=brup.start)]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        out_put(domain)
    else:
        parse.print_help()
        sys.exit(0)

