# coding = utf-8
import requests
import sys

# from demo01.子域名收集.common import get_header, is_domain

sys.path.append("..")
from bs4 import BeautifulSoup
from common import *

crt_base_url = "https://crt.sh/?q="


class Domain_crt(object):
    def __init__(self, domain):
        self._crt_base_url = "https://crt.sh/?q="
        self._domain = domain

    def start(self):
        print("开始运行crt模块")
        re_url = self._crt_base_url + self._domain
        response = requests.get(re_url, headers=get_header())
        html = response.text
        soup = BeautifulSoup(html, "lxml")
        tds = soup.find_all(name="td", attrs={"style": None, "class": None})
        domain_list1 = []
        for td in tds:
            try:
                if is_domain(td.string):  # 是域名的才加入列表
                    domain_list1.append(td.string)
            except Exception as e:
                pass
                # 去重
        domain_list1 = list(set(domain_list1))
        save(data=domain_list1, module="crt", domain=self._domain)
        print("crt模块运行完成！！！")

# domain = "wuyecao.net"
# domain_list = Domain_crt(domain)
# domain_list.start()
