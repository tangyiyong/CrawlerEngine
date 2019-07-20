#!/usr/bin/env python
# -- coding: utf-8 --
import json

import requests
from multiprocessing.pool import ThreadPool

from public.tools import Tools
from fake_useragent import UserAgent


# 指纹扫描
class Feature(object):

    # 构造函数
    def __init__(self):
        super(Feature, self).__init__()

        # 头部信息
        self.headers = {
            'User-Agent': UserAgent(use_cache_server=False).random,
        }

        # 获取指纹数据
        self.data = open('publicdata/data.json', 'r')
        self.cmsdata = json.load(self.data, encoding="utf-8")

    # 找出特征
    def feature(self, site):
        # 遍历检测
        for cmsjson in self.cmsdata:

            # 特征链接
            featureUrl = cmsjson['url']

            # 特征文本
            textRule = cmsjson['re']

            try:
                res = requests.get(site, headers=self.headers, timeout=5)
            except:
                continue

            pageContent = res.text

            if textRule not in pageContent:
                continue

            try:
                res = requests.get(site + featureUrl, headers=self.headers, timeout=5)
                if res.status_code == 200:
                    print("[+] 找到 " + site + " 是一个 " + cmsjson['name'] + " 程序!")
                    Tools.writeFile("feature/output/" + cmsjson['name'] + ".txt", site)
            except:
                continue

    # 开始工作
    def start(self):
        pool = ThreadPool(processes=50)
        pool.map(self.feature, Tools.getFile("domain/output/sites.txt"))
        pool.close()
        pool.join()
