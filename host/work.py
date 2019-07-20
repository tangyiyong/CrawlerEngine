#!/usr/bin/env python
# -- coding: utf-8 --
import socket
import sys
from ipaddress import ip_address
from multiprocessing.pool import ThreadPool
from public.tools import Tools


# 主机扫描
class Host(object):

    # 构造函数
    def __init__(self):
        super(Host, self).__init__()

        # 数值计算
        self.nowCount = 0
        self.maxCount = 0

    # 判断开放
    def host(self, ip):
        # 输出当前进度
        self.nowCount += 1
        sys.stdout.write("[+] 当前进度：{:.2f}%".format(self.nowCount / self.maxCount * 100))
        sys.stdout.write("\r")

        ports = [80, 81, 8000, 8080]

        for port in ports:

            server = (ip, port)
            sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sockfd.settimeout(0.01)
            ret = sockfd.connect_ex(server)

            if not ret:
                Tools.writeFile("host/output/ips.txt", ip + ":" + str(port))
                sockfd.close()
            else:
                sockfd.close()

    # 地址计算
    def ipcount(self, startip, endip):
        start = ip_address(startip)
        end = ip_address(endip)

        ipList = []
        while start <= end:
            ipList.append(str(start))
            start += 1

        return ipList

    # 开始工作
    def start(self):
        Tools.printAscii()

        startip = input("请输入起始地址：")
        endip = input("请输入结束地址：")

        print()
        print("[+] 正在扫描指定地址段中可用的地址...")

        ips = self.ipcount(startip, endip)
        self.maxCount = len(ips)

        pool = ThreadPool(processes=50)
        pool.map(self.host, ips)
        pool.close()
        pool.join()

        self.nowCount = 0
        self.maxCount = 0

        print("[+] 正在扫描指定地址段中可用的地址 done")
