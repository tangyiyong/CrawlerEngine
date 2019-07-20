#!/usr/bin/env python
# -- coding: utf-8 --
import socket
import sys
import time
from multiprocessing.pool import ThreadPool

from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from urllib import request
import geoip2.database
from elasticsearch import Elasticsearch

from public.tools import Tools


# 主机扫描
class Elastic(object):

    # 构造函数
    def __init__(self):
        super(Elastic, self).__init__()

        # 头部信息
        self.headers = {
            'User-Agent': UserAgent().random,
        }

        # 国家数据
        self.reader = geoip2.database.Reader('publicdata/geolite2.mmdb')

        # 数据保存
        self.es = Elasticsearch(["127.0.0.1:9200"])

        # 数值计算
        self.nowCount = 0
        self.maxCount = 0

    # 主机特征
    def collectHost(self, ip):
        # 输出当前进度
        self.nowCount += 1
        sys.stdout.write("[+] 当前进度：{:.2f}%".format(self.nowCount / self.maxCount * 100))
        sys.stdout.write("\r")

        # 分割地址
        realip = ip.split(":")[0]
        port = ip.split(":")[1]

        # 获取响应
        try:
            req = request.Request("http://" + ip, headers=self.headers)
            resp = request.urlopen(req, timeout=5)
        except:
            return

        response = "HTTP/1.1 "
        response += str(resp.status) + " " + resp.reason + "\n"
        response += str(resp.info()) + "\n\n"

        try:
            html = resp.read().decode('utf-8')
            response += html
        except:
            return

        # 获取国家
        country = self.reader.country(realip)
        country = country.country.name

        # 获取状态码
        statecode = str(resp.status)

        # 获取标题
        soup = BeautifulSoup(html.replace("\r\n", ""), "lxml")

        try:
            title = soup.title.string
        except:
            title = "Unknow"

        # 更新时间
        updatetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # 获取服务
        server = resp.getheader(name="Server")

        # 获取操作系统
        # ...

        body = {
            "ip": realip,
            "domain": "",
            "port": port,
            "title": title,
            "country": country,
            "server": server,
            'statecode': statecode,
            "response": response,
            "updatetime": updatetime,
        }

        self.es.index(index="sadness", doc_type="doc", body=body)

    # 开始工作
    def startHost(self):
        print("[+] 正在提取可用地址的特征...")

        ips = Tools.getFile("host/output/ips.txt")
        self.maxCount = len(ips)

        pool = ThreadPool(processes=50)
        pool.map(self.collectHost, ips)
        pool.close()
        pool.join()

        self.nowCount = 0
        self.maxCount = 0

        print("[+] 正在提取可用地址的特征 done")

    # 域名特征
    def collectSite(self, site):
        # 输出当前进度
        self.nowCount += 1
        sys.stdout.write("[+] 当前进度：{:.2f}%".format(self.nowCount / self.maxCount * 100))
        sys.stdout.write("\r")

        # 获取响应
        try:
            req = request.Request(site, headers=self.headers)
            resp = request.urlopen(req, timeout=5)
        except:
            return

        response = "HTTP/1.1 "
        response += str(resp.status) + " " + resp.reason + "\n"
        response += str(resp.info()) + "\n\n"

        # 网站编码

        try:
            encoding = resp.getheader(name="Content-Type").split("=")[1]
        except:
            encoding = "utf-8"

        try:
            html = resp.read().decode(encoding)
            response += html
        except:
            return

        try:
            myaddr = socket.getaddrinfo(site[0:-1].replace("http://"), 80)
            realip = myaddr[0][4][0]

            # 获取国家
            country = self.reader.country(realip)
            country = country.country.name
        except:
            realip = "Unknow"
            country = "Unknow"

        # 获取状态码
        statecode = str(resp.status)

        # 获取标题
        soup = BeautifulSoup(html.replace("\r\n", ""), "lxml")

        try:
            title = soup.title.string
        except:
            title = "Unknow"

        # 更新时间
        updatetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # 获取服务
        server = resp.getheader(name="Server")

        # 获取操作系统
        # ...

        body = {
            "ip": realip,
            "domain": site,
            "port": "80",
            "title": title,
            "country": country,
            "server": server,
            'statecode': statecode,
            "response": response,
            "updatetime": updatetime,
        }

        self.es.index(index="sadness", doc_type="doc", body=body)

    # 开始工作
    def startSite(self):
        print("[+] 正在提取所有域名的特征...")

        sites = Tools.getFile("domain/output/sites.txt")
        self.maxCount = len(sites)

        pool = ThreadPool(processes=50)
        pool.map(self.collectSite, sites)
        pool.close()
        pool.join()

        self.nowCount = 0
        self.maxCount = 0

        print("[+] 正在提取所有域名的特征 done")
        print()

        input("按任意键继续...")
