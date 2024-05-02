# -*- coding: utf-8 -*-
import json
from typing import Any
from typing_extensions import Self

import scrapy
from scrapy import Request
from scrapy import signals
from scrapy.crawler import Crawler

from shares_scrapy.items import SharesItem
from shares_scrapy.common.echo import echo_info
from shares_scrapy.model import T, areas_story, csrcs_story




class GetSharesSpider(scrapy.Spider):
    name = "get_shares"
    allowed_domains = ["sina.com.cn"]
    start_urls = ["https://vip.stock.finance.sina.com.cn/mkt/"]
    url_model = ('https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData'
                 '?page={}&num=80&sort=symbol&asc=1&node={}&symbol=&_s_r_a=page')
    all_target = {'area': areas_story.all_areas(), 'csrc': csrcs_story.all_csrcs(level=2)}

    def __init__(self, target='area', *args, **kwargs):
        """
        重写构造函数
        :param target:  spider传参数,area指通过地域查询,csrc指通过行业查询
            传参命令:scrapy crawl get_shares -a target=csrc
        :param args:    父类参数
        :param kwargs:  父类参数
        """
        super(GetSharesSpider, self).__init__(*args, **kwargs)
        # super().__init__(*args, **kwargs) 新格式
        self.target = target

    def parse(self, response, *args, **kwargs):
        """
        访问默认页,组装股票条数查询URL
        :param response:
        :param args:
        :param kwargs:
        """
        count_url = ('https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center'
                    '.getHQNodeStockCount?node={}')
        for row in self.all_target[self.target].values():
            # 组装获取股票数量地址
            now_url = count_url.format(row['code'])
            yield Request(url=now_url, callback=self.parse_count, meta={'code': row['code'], 'id': row['id']})

    def parse_count(self, response):
        """
        获取股票数量,组装获取股票信息地址
        :param response: meta['code'','id'] code:要查询的地域或者行业code,id为对应的本系统id
        """
        code = response.meta.get("code")
        target_id = response.meta.get('id')
        result_json = json.loads(response.body)
        if len(result_json) <= 0: return None
        pages = int(json.loads(response.body)) // 80
        for page in range(1, pages + 2):
            now_url = self.url_model.format(page, code)
            yield Request(url=now_url, callback=self.parse_gain if self.target == 'area' else self.parse_update,
                          meta={'id': target_id})

    def parse_gain(self, response):
        """
        通过地域获取每支股票基础信息
        :param response: meta['id'] 为area_id
        """
        item = SharesItem()
        data = json.loads(response.body)
        item_keys = item.fields.keys()
        area_id = response.meta.get('id')
        # 数据库与新浪字段一一对应
        one_to_one = {'new_price': 'trade', 'min_price': 'low', 'max_price': 'high', 'open_price': 'open',
                      'last_price': 'settlement', 'price_change': 'pricechange', 'change_percent': 'changepercent'}
        for share in data:
            for key in item_keys:
                if key == 'id' or key == 'csrc_id':
                    continue
                elif key == 'area_id':
                    item[key] = area_id
                elif key in one_to_one.keys():
                    item[key] = share[one_to_one[key]]
                else:
                    item[key] = share[key]

            yield item

    def parse_update(self, response):
        """
        修改股票证监会行业分类
        :param response: meta['id'] 为csrc_id
        """
        csrc_id = response.meta.get('id')
        all_data = json.loads(response.body)
        for share in all_data:
            share_update = T.shares.update().where(T.shares.c.name == share['name']).values(csrc_id=csrc_id)
            result = T.connect.execute(share_update)
            echo_info(share['name'], result.rowcount)

    @staticmethod
    def save_data(sender, item, response, spider):
        echo_info('spider', '传递数据到item {}'.format(item['code']))

    @staticmethod
    def spider_error(failure, spider):
        echo_info('error', '{} error {}'.format(spider.name, failure))

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(cls.save_data, signals.item_scraped)        # item数据提取信号
        crawler.signals.connect(cls.spider_error, signals.spider_error)     # 错误信号,如超时,连接错误等
        return spider

