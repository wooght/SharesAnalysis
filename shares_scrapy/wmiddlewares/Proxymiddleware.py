# -- coding: utf-8 -
"""
@project    :shares_scrapy
@file       :Proxymiddleware.py
@Author     :wooght
@Date       :2024/5/14 11:56
@Content    :代理中间件
"""
import random
from scrapy.exceptions import IgnoreRequest
from shares_scrapy.model import proxy_sitory
import sys
sys.path.append(r'E:\wooght-server\scripy_wooght\shares_scrapy\shares_scrapy')
from main import get_ips

class ProxyMiddleware:
    def __init__(self, crawler):
        self.crawler = crawler
        self.all_ip = proxy_sitory.all_proxy()
        self.now_ip = ''
        self.get_ip_nums = 0
        self.get_ip()

    @classmethod
    def from_crawler(cls, crawler):
        print('加载proxymiddleware')
        return cls(crawler)

    def process_request(self, request,spider):
        """
            设置代理IP
        :param request:
        :param spider:
        :return:
        """
        if 'proxy_status' not in request.meta.keys(): return None
        if len(self.now_ip) == 0: raise IgnoreRequest('无代理IP可选')
        request.meta['proxy'] = 'http://{}'.format(self.now_ip)
        print('代理访问{},IP:{}'.format(request.url, self.now_ip))

    def process_exception(self, request, exception, spider):
        """
            捕获代理异常
            切换IP
        :param request:
        :param exception:
        :param spider:
        TCPTimedOutError  ValueError
        """
        print('proxymiddle 捕获错误{},url:{}'.format(exception.__class__.__name__, request.url))
        if 'proxy' in request.meta.keys():
            self.change_ip()
        return None

    def process_response(self, request, response, spider):
        print('代理返回response状态为:{}'.format(response.status))
        return response

    def get_ip(self):
        self.all_ip = proxy_sitory.all_proxy()
        if len(self.all_ip) < 3:
            self.more_ip()
        if len(self.all_ip) == 0:
            self.now_ip = ''
            return False
        self.now_ip = random.choice(self.all_ip)
        proxy_sitory.set_lock(self.now_ip)
        return True

    def more_ip(self):
        self.get_ip_nums += 1
        result = get_ips.delay()
        print('获取代理IP spider开启,ID{}'.format(result.id))


    def change_ip(self):
        i = self.all_ip.index(self.now_ip)
        del self.all_ip[i]
        proxy_sitory.set_unenabled(self.now_ip)
        self.get_ip()

