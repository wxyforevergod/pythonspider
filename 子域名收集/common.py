# coding = utf-8
# coding = utf-8
# 存放公共函数
import json
import os.path
import re

import requests
from fake_useragent import UserAgent
import time
from config import *


def is_domain(domain):
    """
    判断是否是有效域名
    :param domain:
    :return:
    """
    pattern = re.compile(
        r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|'
        r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|'
        r'([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9])).'
        r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3})$'
    )
    return True if pattern.match(domain) else False


def get_header():
    """
    设置随机UA
    :return:
    """
    ua = UserAgent()
    headers = {
        "User-Agent": ua.random
    }
    return headers


def get_url(url):
    """
    获取随机请求头
    :param url:
    :return:
    """
    # 获取随机头
    headers = get_header()
    # 发起请求
    try:
        response = requests.get(url, headers=headers, timeout=2)
        return response
    except Exception as e:
        pass


def make_dir(path):
    """
    判断文件路径是否存在，不存在就创建
    :param path:
    :return:
    """
    if not os.path.exists(path):
        # 创建目录
        os.makedirs(path)


def save(**dict):
    """
    base_path : ./cache
    保存为json数据
    path = ./cache/模块/域名/域名.时间.json
    :param dict: 动态参数：data moudel domain
    :return:
    """
    # 分别获取数据
    data = dict['data']
    module = dict['module']
    domain = dict['domain']
    if data is not None and module is not None and domain is not None:
        # 创建文件夹
        save_path = cache_base_path + module + "/" + domain + "/"
        make_dir(save_path)
        # 准备完整路径
        save_path = save_path + domain + "." + str(time.time()) + ".json"
        # 保存数据
        with open(save_path, "a+") as f:
            json.dump(data, f, indent=4)


def out_put(domain):
    domain_unique = []
    # 准备路径
    for m in module_list:
        path = cache_base_path + m + "/" + domain
        if os.path.exists(path):
            # 读取文件，只需获取最新生成的文件
            files = os.listdir(path)
            # 去最新的文件
            file = files[-1]
            # 读取文件
            print(file)
            with open(path + "/" + file, "r") as f:
                data = json.load(f)
                domain_unique += data
                print(data)
    # 去重
    domain_unique = list(set(domain_unique))
    # 将domain_unique保存到文件中
    if os.path.exists("./domain.txt"):
        os.remove("./domain.txt")
    with open("./domain.txt", "w") as f:
        for d in domain_unique:
            f.write(d + "\n")
