# -- coding: utf-8 -
"""
@project    :shares_scrapy
@file       :meituan_shouyin.py
@Author     :wooght
@Date       :2024/4/25 20:42
@Content    :美团收银爬虫
"""
from typing import Iterable

import scrapy
from scrapy import FormRequest, Request
from shares_scrapy.common.SecretCode import Wst
from shares_scrapy.common.DateTimeMath import WDate
import time

class MeituanShouyinSpider(scrapy.Spider):
    name = "meituan_shouyin"
    turnover_api_model = 'https://retailadmin-erp.meituan.com/api/report/revenue/data?startTime={}&endTime={}&cashier_id=-1&yodaReady=h5&csecplatform=4&csecversion=2.4.0'

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            "shares_scrapy.middlewares.SharesScrapyDownloaderMiddleware": None,
            "shares_scrapy.wmiddlewares.Marketmiddleware.Marketmiddleware": None,
            "shares_scrapy.wmiddlewares.Proxymiddleware.ProxyMiddleware": None,
            "shares_scrapy.wmiddlewares.Shouyinmiddleware.ShouyinMiddleWare": 343
        }
    }

    def start_requests(self) -> Iterable[Request]:
        start_day = WDate.before_day(30)
        url = self.turnover_api_model.format(str(start_day[1]) + '000', str(int(WDate.time_stamp)) + '999')
        yield Request(url=url, callback=self.parse, errback=self.err_parse)

    def parse(self, response, *args):
        print('返回parse')
        # cc = response.headers.getlist("Set-Cookie")
        # for c in cc:
        #     print(c)
        print(response.body.decode('utf-8'))

    #
    # def parse_api(self, response):
    #     if '商品' in response.body.decode('utf-8'):
    #         print('登录成功')
    #         start_day = WDate.before_day(30)
    #         url = self.turnover_api_model.format(str(start_day[1]) + '000', str(int(WDate.time_stamp)) + '999')
    #         yield Request(url=url, callback=self.parse_turnover)
    #     else:
    #         print('登录返回状态:{}'.format(response.status))
    #         print(response.body.decode('utf-8'))
    #
    # def parse_turnover(self, response):
    #     print(response.body.decode('utf-8'))

    def err_parse(self, failure):
        print(failure.request.url)
        print(failure.value.__class__.__name__)

