# -- coding: utf-8 -
"""
@project    :shares_scrapy
@file       :extensions.py
@Author     :wooght
@Date       :2024/5/2 19:52
@Content    :扩展,信号绑定
"""
from scrapy import signals
from shares_scrapy.common.echo import echo_info

class ProcessExtension:
    def __init__(self, crawler):
        self.crawler = crawler
        # 注册信号
        self.crawler.signals.connect(self.spider_start, signals.spider_opened)
        self.crawler.signals.connect(self.spider_stop, signals.spider_closed)
        self.crawler.signals.connect(self.engine_start, signals.engine_started)
        self.crawler.signals.connect(self.engine_stop, signals.engine_stopped)
        """
            其他信号:
                request_scheduled   请求发送前信号
                response_received   接受相应后信号
                item_scraped        提取数据信号
        """

    @classmethod        # 类方法   此写法叫做装饰器
    def from_crawler(cls, crawler):
        return cls(crawler)

    def spider_start(self, spider):
        echo_info('extension', '{} star'.format(spider.name))

    def spider_stop(self, spider):
        echo_info('extension', '{} closed'.format(spider.name))

    def engine_start(self):
        echo_info('extension', 'engine start')

    def engine_stop(self):
        echo_info('extension', 'engine stop')