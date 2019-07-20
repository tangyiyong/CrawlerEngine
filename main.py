#!/usr/bin/env python
# -- coding: utf-8 --

import os

from crawler.work import Crawler
from elastic.search import MyElasticSearch
from public.tools import Tools

if __name__ == '__main__':

    while True:
        os.system("cls")
        Tools.printAscii()
        print("1. 采集指纹")
        print("2. 检索指纹")
        print("3. 清除缓存")
        print("4. 退出程序")
        print()
        choise = int(input("请选择一个模式："))

        if choise == 1:
            Crawler().start()
        elif choise == 2:
            MyElasticSearch().search()
        elif choise == 3:
            Tools().clearAll()
        elif choise == 4:
            break
        else:
            continue
