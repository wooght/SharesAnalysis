# -*- coding: utf-8 -*-
import json
from typing import Iterable

import scrapy
from scrapy import Request
from shares_scrapy.items import AreaItem, Csrcclassify


class SinashareSpider(scrapy.Spider):
    name = "Sinashare"
    allowed_domains = ["sina.com.cn"]
    start_urls = ["https://vip.stock.finance.sina.com.cn/mkt/"]
    market_center = {}
    market_dict = {}

    # def start_requests(self):
    #     temp_url = "https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodes"
    #     R = scrapy.Request(temp_url, callback=self.parse)

    def parse(self, response, **kwargs):
        """
        爬取所有A股结构
        :名称,代码,证监局分类,地域
        """
        temp_url = "https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodes"
        R = scrapy.Request(temp_url, callback=self.temp_parse)
        yield R

    def temp_parse(self, response):
        items = AreaItem()
        json_str = response.body.decode('utf8')
        json_obj = json.loads(json_str)
        self.get_market_center(json_obj)
        all_areas = self.market_center['地域板块']
        for row in all_areas:
            items['name'] = row[0]
            items['sina_code'] = row[2]
            yield items

    def get_market_center(self, obj):
        if isinstance(obj, list):
            for key in range(len(obj)):
                if obj[key] in ["地域板块","证监会行业"]:
                    self.market_center[obj[key]] = obj[key+1]
                else:
                    self.get_market_center(obj[key])

