# -- coding: utf-8 -
"""
@project    :shares_scrapy
@file       :xueqiu_sign.py
@Author     :wooght
@Date       :2024/5/14 22:53
@Content    :redis 操作
"""
import scrapy


class XueqiuSignSpider(scrapy.Spider):
    name = "xueqiu_sign"
    start_urls = ['https://mp.xueqiu.com/']
    allowed_domains = ["xueqiu.com"]
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            "shares_scrapy.middlewares.SharesScrapyDownloaderMiddleware": 510,
            "shares_scrapy.wmiddlewares.Xueqiumiddleware.XueqiuMiddleware": 543
        }
    }

    def parse(self, response, *args):
        print(response.body.decode('utf-8'))
        yield scrapy.Request(url='https://xueqiu.com/hot_event/list.json?count=10', callback=self.parse_json)


    def parse_json(self, response):
        print(response.body.decode('utf-8'))



    """
        Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36
        https://xueqiu.com/recommend-proxy/feed_etf.json?source=etf&max_id=290526220&last_id=290526220&page=6&_=1717508672045
        https://xueqiu.com/recommend-proxy/feed_etf.json?source=etf&max_id=291240442&last_id=291240442&page=5&_=1717508672040
    """
