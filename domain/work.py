#!/usr/bin/env python
# -- coding: utf-8 --
import sys

import requests
from multiprocessing.pool import ThreadPool

from public.tools import Tools
from fake_useragent import UserAgent

from bs4 import BeautifulSoup


# 主机扫描
class Domain(object):

    # 构造函数
    def __init__(self):
        super(Domain, self).__init__()

        # 头部信息
        self.agent = UserAgent(use_cache_server=False)
        self.agent = UserAgent(verify_ssl=False)
        self.agent = UserAgent(cache=False)

        self.headers = {
            'User-Agent': self.agent.random,
        }

        # 数值计算
        self.nowCount = 0
        self.maxCount = 0

    # 找出特征
    def domain(self, ip):
        # 输出当前进度
        self.nowCount += 1
        sys.stdout.write("[+] 当前进度：{:.2f}%".format(self.nowCount / self.maxCount * 100))
        sys.stdout.write("\r")

        try:
            r = requests.get("https://site.ip138.com/" + ip, headers=self.headers, timeout=5)
        except:
            return

        soup = BeautifulSoup(r.text, "lxml")
        links = soup.select("ul#list > li > a")

        if len(links) == 0:
            return None

        for link in links:
            Tools.writeFile("domain/output/sites.txt")

    # 开始工作
    def start(self):
        print("[+] 正在反查所有域名记录...")

        ips = Tools.getFile("host/output/ips.txt")
        self.maxCount = len(ips)

        pool = ThreadPool(processes=50)
        pool.map(self.domain, ips)
        pool.close()
        pool.join()

        self.nowCount = 0
        self.maxCount = 0

        print("[+] 正在反查所有域名记录 done")
