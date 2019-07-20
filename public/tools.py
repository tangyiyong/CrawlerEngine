#!/usr/bin/env python
# -- coding: utf-8 --

# 工具类
import os
from elasticsearch import Elasticsearch


class Tools(object):

    def __init__(self):
        pass

    # 写入文件
    @staticmethod
    def writeFile(filename, content):
        f = open(filename, "a")
        f.write(content + "\n")
        f.close()

    # 获取文件
    @staticmethod
    def getFile(filename):
        tempList = []
        f = open(filename, "r")
        for line in f.readlines():
            tempList.append(line.strip("\n"))
        f.close()
        return tempList

    # 打印标记
    @staticmethod
    def printAscii():
        os.system("cls")
        print('''.oPYo.                                     8 .oPYo.               o              
8    8                                     8 8.                                  
8      oPYo. .oPYo. o   o   o .oPYo. oPYo. 8 `boo   odYo. .oPYo. o8 odYo. .oPYo. 
8      8  `' .oooo8 Y. .P. .P 8oooo8 8  `' 8 .P     8' `8 8    8  8 8' `8 8oooo8 
8    8 8     8    8 `b.d'b.d' 8.     8     8 8      8   8 8    8  8 8   8 8.     
`YooP' 8     `YooP8  `Y' `Y'  `Yooo' 8     8 `YooP' 8   8 `YooP8  8 8   8 `Yooo' 
:.....:..:::::.....:::..::..:::.....:..::::..:.....:..::..:....8 :....::..:.....:
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::ooP'.::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::...::::::::::::::::::''')
        print()

    # 清除文件
    @staticmethod
    def delfile(path):
        dirfiles = os.listdir(path)
        for dirfile in dirfiles:
            cpath = os.path.join(path, dirfile)
            if os.path.isdir(cpath):
                Tools.delfile(cpath)
            else:
                os.remove(cpath)

    # 清除所有
    @staticmethod
    def clearAll():
        Tools.printAscii()

        # 清除数据库
        es = Elasticsearch(["127.0.0.1:9200"])
        body = {'query': {'match_all': {}}}
        es.delete_by_query(index="sadness", body=body)

        # 清除文件
        Tools.delfile("domain/output")
        Tools.delfile("feature/output")
        Tools.delfile("host/output")

        print("[+] 删除所有缓存文件成功！")
        print()

        input("按任意键继续...")
