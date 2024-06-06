# -- coding: utf-8 -
"""
@project    :shares_scrapy
@file       :dont_close.py
@Author     :wooght
@Date       :2024/4/25 20:42
@Content    :借助空闲信号实现等待新的请求
"""
from typing import Any
from typing_extensions import Self
from scrapy.exceptions import DontCloseSpider

from scrapy import signals, Request, Spider
from scrapy.crawler import Crawler


class DontClose(Spider):
    """
    实现无新的request情况下不关闭spider,而等待新的request的功能
    signals.spider_idle指空闲信号,无请求的时候,引擎会先发出空闲信号,再发出关闭信号
    DontCloseSpider 不能关闭spider的异常,触发此异常后,引擎又会发出空闲信号
    流程:signals.spider_idle-->获取新的request-->DontCloaseSpider-->signals.spider_idle 循环此流程
    """
    name = "dont_close"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]
    idle_second = 0  # 空闲信号次数
    url_pool = []
    step = 3

    def __init__(self, crawler, *args, **kwargs):
        """
        利用够着函数,将crawler带入本实例中,为后期crawler.engine.crawl做准备
        :param crawler:
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        self.crawler = crawler


    @classmethod
    def from_crawler(cls, crawler: Crawler, *args: Any, **kwargs: Any) -> Self:
        """
        构造带crawler的spider实例
        :param crawler:scrapy 的爬虫核心
        :param args:
        :param kwargs:
        :return: cls
        """
        spider = cls(crawler)
        crawler.signals.connect(spider.idle, signal=signals.spider_idle)                    # spider_idle 空闲信号绑定
        crawler.signals.connect(spider.parse_err, signal=signals.spider_error)              # spider错误信号绑定
        crawler.signals.connect(spider.request_scheduled, signal=signals.request_scheduled) # request_scheduled 请求排入队列信号
        return spider

    def parse(self, response, *args):
        self.url_pool = response.css("a.tag::attr(href)").extract()
        for url in self.url_pool[:self.step]:
            yield Request(url=response.urljoin(url), callback=self.get_body)

    def get_body(self, response):
        print(response.url, response.ip_address)

    def idle(self):
        """
        爬虫空闲回调函数,作为新请求入口
        :return: return 则停止爬虫
        """
        self.idle_second += 1
        if self.idle_second % 5 == 0:
            current_second = self.idle_second // 5
            print(current_second)
            if current_second >= len(self.url_pool):
                print('spider to closed')
                return
            else:
                print('get new request')
                self.get_new_request()

        print('空闲状态{}'.format(self.idle_second))
        # 抛出不关闭spider的核心异常,DontCloseSpider 唯一功能是不关闭spider,引擎则会按照同域访问间隔发出空闲信号
        raise DontCloseSpider

    def request_scheduled(self, request):
        print('new url scheduled,', request.url)

    def parse_err(self):
        print('error')
        print(self.idle_second)

    def get_new_request(self):
        """
        构建新请求,并交由engine进行crawl爬取
        不能用yield进行提交请求,因为engine处于空闲状态,此时调度和引擎是断开的
        """
        new_url = '{}{}'.format(self.start_urls[0], self.url_pool[self.idle_second // 5])
        print('new url :'.format(new_url))
        new_request = Request(url=new_url, callback=self.get_body, errback=self.parse_err)
        # 将新request直接交由引擎进行爬取
        self.crawler.engine.crawl(new_request)





