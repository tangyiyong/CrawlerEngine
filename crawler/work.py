from domain.work import Domain
from elastic.work import Elastic
from host.work import Host


# 采集指纹
class Crawler(object):

    # 构造函数
    def __init__(self):
        super(Crawler, self).__init__()

    # 流水线
    def start(self):
        # 主机扫描
        Host().start()

        # 地址指纹
        Elastic().startHost()

        # 域名扫描
        Domain().start()

        # 域名特征
        Elastic().startSite()
