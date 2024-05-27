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
from shares_scrapy.common.DateTimeMath import WDate

class MeituanShouyinSpider(scrapy.Spider):
    name = "meituan_shouyin"
    turnover_api_model = 'https://retailadmin-erp.meituan.com/api/report/revenue/data?startTime={}&endTime={}&cashier_id=-1&yodaReady=h5&csecplatform=4&csecversion=2.4.0'
    turnover_list_api = 'https://retailadmin-erp.meituan.com/api/report/revenue/trend?begin_datekey={}&end_datekey={}&isRT=false&cashier_id=-1&yodaReady=h5&csecplatform=4&csecversion=2.4.0'
    classify_api = 'https://retailadmin-erp.meituan.com/api/goods/category'
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
        turnover_class_url = self.turnover_api_model.format(str(start_day[1]) + '000', str(int(WDate.time_stamp)) + '999')
        turnover_list_url = self.turnover_list_api.format(str(start_day[0].replace('-', '')), str(WDate.now_date).replace('-', ''))
        yield Request(url=turnover_class_url, callback=self.parse, errback=self.err_parse)
        yield Request(url=turnover_list_url, callback=self.parse_list, errback=self.err_parse)
        yield Request(url=self.classify_api, callback=self.parse_classify, errback=self.err_parse)

    def parse(self, response, *args):
        print('返回parse')
        # cc = response.headers.getlist("Set-Cookie")
        # for c in cc:
        #     print(c)
        print(response.body.decode('utf-8'))

    def parse_list(self, response):
        print('返回parse_list')
        print(response.body.decode('utf-8'))

    def parse_classify(self, response):
        print('返回到parse_classify')
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

"""
    地址:
        营业员:
        https://retailadmin-erp.meituan.com/api/report/employee/getAllEmployee?yodaReady=h5&csecplatform=4&csecversion=2.4.0
        营业额:
        https://retailadmin-erp.meituan.com/api/report/revenue/data?startTime=1716739200000&endTime=1716786900000&cashier_id=-1&yodaReady=h5&csecplatform=4&csecversion=2.4.0
        一天营业额走势:
        https://retailadmin-erp.meituan.com/api/report/revenue/trend?begin_datekey=20240527&end_datekey=20240527&isRT=true&cashier_id=-1&yodaReady=h5&csecplatform=4&csecversion=2.4.0
        历史走势:
        https://retailadmin-erp.meituan.com/api/report/revenue/trend?begin_datekey=20240501&end_datekey=20240527&isRT=false&cashier_id=-1&yodaReady=h5&csecplatform=4&csecversion=2.4.0
        分类:
        https://retailadmin-erp.meituan.com/api/goods/category
        
        https://retailadminapi-erp.meituan.com/api/v2/goods?pageNo=1&pageSize=20&categoryId=10165598&yodaReady=h5&csecplatform=4&csecversion=2.4.0&mtgsig={"a1":"1.1","a2":1716810080285,"a3":"z936y4z9u3w25u1117282v2x0uwuyx2y810wwzu75xy9795840wz4z50","a5":"XqHjNT/9DEbYT1CuIu2FfjY7qMgZoVYt","a6":"hs1.4a4gsvX1s4RLQYqBR3sFhAWSlO5UWEFWdRdeo/eFOqtevDxopk43DFZK4Ya2yRc5ryhIkIlj0pUo89CLRxB6H7B1RqfJGb8K2JSFu4X1txBk=","x0":4,"d1":"49777c3b4d80f305cd86000b04f78f3c"}
"""