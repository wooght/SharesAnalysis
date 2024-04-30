# -- coding: utf-8 -
"""
@project    :shares_scrapy
@file       :Marketsituation.py
@Author     :wooght
@Date       :2024/4/25 20:42
@Content    :获取历史行情日K
"""
from typing import Iterable

import scrapy
from scrapy import Request
from shares_scrapy.common.echo import echo
import json
from shares_scrapy.model import T, shares_story, marketes_story
from shares_scrapy.common.DateTimeMath import WDate
from shares_scrapy.items import MarketItem


class MarketsituationSpider(scrapy.Spider):
    name = "Marketsituation"
    allowed_domains = ["sina.com.cn"]
    start_urls = ["https://sina.com.cn"]
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES':{
            "shares_scrapy.middlewares.SharesScrapyDownloaderMiddleware": None,
            "shares_scrapy.wmiddlewares.Marketmiddleware.Marketmiddleware": 543
        }
    }
    url_models = 'https://finance.sina.com.cn/realstock/company/{share}/hisdata_klc2/klc_kl.js?d={now_date}'

    def start_requests(self):
        # @returns requests 0 10
        echo('从这里开始')
        all_shares = shares_story.all_shares()
        now_date = WDate.now_date.replace('-', '_')
        exists_market = marketes_story.group_code() if marketes_story.group_code() else []
        for share in all_shares:
            if share.code in exists_market: continue
            yield Request(url=self.url_models.format(share=share.symbol, now_date=now_date),
                          callback=self.parse, meta={'id':share.id, 'code': share.code}, errback=self.parse_err)

    def parse(self, response, *args, **kwargs):
        item = MarketItem()
        stack_data = json.loads(response.body)
        meta = {'share_id': response.meta['id'], 'code': response.meta['code']}
        echo(meta['code'], len(stack_data))
        for stack in stack_data:
            item['share_id'] = meta['share_id']
            item['code'] = meta['code']
            for key, value in stack.items():
                item[key] = value
            yield item

    def parse_err(self, response):
        echo(response.url)