# -*- coding: utf-8 -*-
import json
from typing import Iterable

import scrapy
from scrapy import Request
from shares_scrapy.items import AreaItem, Csrcclassify
from shares_scrapy.common.echo import echo


class SinashareSpider(scrapy.Spider):
    name = "Sinashare"
    allowed_domains = ["sina.com.cn"]
    start_urls = ["https://vip.stock.finance.sina.com.cn/mkt/"]
    market_center = {}

    # def start_requests(self):
    #     yield Request(url=self.start_urls[0], callback=self.parse)

    def parse(self, response, **kwargs):
        echo('访问基本信息:', response.url)
        """
        爬取所有A股结构
        :名称,代码,证监局分类,地域
        通过行业获取股票代码:
        https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=80&sort=symbol&asc=1&node=hangye_ZF51&symbol=&_s_r_a=init
        通过地域获取股票代码:
        https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=2&num=80&sort=symbol&asc=1&node=diyu_510000&symbol=&_s_r_a=page
        """
        temp_url = "https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodes"
        yield Request(temp_url, callback=self.market_parse)

    def market_parse(self, response):
        echo(response.url+' 访问成功!')
        items = AreaItem()
        csrc_item = Csrcclassify()
        json_str = response.body.decode('utf8')
        json_obj = json.loads(json_str)
        self.get_market_center(json_obj)
        all_areas = self.market_center['地域板块']
        all_classify = self.get_csrcclassify(self.market_center['证监会行业'])
        for value in all_areas:
            items['name'] = value[0]
            items['sina_code'] = value[2]
            print(items)
            yield items
        for key, value in all_classify.items():
            for j in value.keys():
                csrc_item[j] = value[j]
            yield csrc_item

    def get_market_center(self, obj):
        if isinstance(obj, list):
            for key in range(len(obj)):
                if obj[key] in ["地域板块", "证监会行业"]:
                    self.market_center[obj[key]] = obj[key+1]
                else:
                    self.get_market_center(obj[key])

    def get_csrcclassify(self, data):
        print(data)
        result_dict = {}
        for item in data:
            result_dict[item[0]] = {'name': item[0], 'parent_id': -1, 'sina_code': item[3]}
            for val in item[1]:
                if val[0] in result_dict.keys(): continue
                result_dict[val[0]] = {'name': val[0], 'parent_id': item[0], 'sina_code': val[2]}
        print(result_dict)
        return result_dict
