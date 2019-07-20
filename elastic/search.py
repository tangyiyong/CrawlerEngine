#!/usr/bin/env python
# -- coding: utf-8 --

from elasticsearch import Elasticsearch

# 主机检索
from public.tools import Tools


class MyElasticSearch(object):

    # 构造函数
    def __init__(self):
        super(MyElasticSearch, self).__init__()

        self.es = Elasticsearch(["127.0.0.1:9200"])
        self.doc_type = "doc"
        self.search_type = ["ip", "title", "server", "country", "port", "response", ]

    # 语法解析
    def queryParser(self, query):
        tmp = query.split(' ')
        resList = []
        for x in tmp:
            if x.count(':') == 0:
                resList.append(x)
            else:
                x = x.replace('+', ' ')
                meta = x.split(':')
                resList.append({"term": {meta[0]: meta[1]}})
        return resList

    # 查询函数
    def search(self):
        Tools.printAscii()

        keyword = input("请输入关键字：")
        fromCount = input("从第几页开始：")
        itemCount = input("查询几条记录：")
        isSave = input("是否同时保存：")
        print()

        # 语法解析
        query = self.queryParser(keyword)

        body = {
            "query": {
                "bool": {
                    "must": query
                }
            },
            "from": fromCount,
            "size": itemCount
        }

        res = self.es.search(index="sadness", body=body)

        if res['hits']['total']['value'] == "0":
            print("[-] 没有找到相关记录！")
        else:
            infoList = []
            for host in res[u'hits']['hits']:
                obj = host['_source']
                infoList.append(obj)

            # 只输出IP地址，或者域名
            for info in infoList:
                if info['domain'] != "":
                    temp = info['domain'] + ":" + info['port']
                else:
                    temp = "http://" + info['ip'] + ":" + info['port']

                if isSave != "0":
                    Tools.writeFile("elastic/output/elastic.txt", temp)

                print("[+] " + temp)

        print()
        input("请按任意键继续...")
