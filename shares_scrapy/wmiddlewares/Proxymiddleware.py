# -- coding: utf-8 -
"""
@project    :shares_scrapy
@file       :Proxymiddleware.py
@Author     :wooght
@Date       :2024/5/14 11:56
@Content    :代理中间件
"""
from scrapy.exceptions import IgnoreRequest
from shares_scrapy.model import proxy_sitory
from shares_scrapy.run.GetProxy import GetProxy

class ProxyMiddleware:
    proxy_ip = GetProxy('proxy_ips')

    def __init__(self, crawler):
        print('ProxyMiddleware 加载成功')
        self.crawler = crawler
        self.current_ip = self.proxy_ip.get_ip()

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
        if len(self.current_ip) == 0: raise IgnoreRequest('无代理IP可选')
        request.meta['proxy'] = 'http://{}'.format(self.current_ip)
        print('代理访问{},IP:{}'.format(request.url, self.current_ip))

    def process_exception(self, request, exception, spider):
        """
            捕获代理异常
            切换IP
        :param request:
        :param exception:
        :param spider:
        TCPTimedOutError  ValueError    TunnelError     MaxRetryError
        """
        print('proxymiddle 捕获错误{},url:{}'.format(exception.__class__.__name__, request.url))
        if 'proxy' in request.meta.keys():
            current_ip = self.proxy_ip.get_ip()
            self.current_ip = current_ip if current_ip else 0
        return None

    def process_response(self, request, response, spider):
        print('{}代理返回response状态为:{}'.format(spider.name, response.status))
        return response


